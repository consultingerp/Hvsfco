# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError, UserError
from datetime import date, datetime, timedelta


class HospitalizationPackage(models.Model):
    _name = "hospitalization.package"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Package'

    @api.multi
    def _claim_count(self):
        for rec in self: 
            rec.package_count = self.env['hms.insurance.claim'].search_count([('package_id', '=', rec.id)])

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the order.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.company_id.currency_id.round(amount_untaxed),
                'amount_tax': order.company_id.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })

    name = fields.Char(string='Name')
    start_date = fields.Datetime("Start Date")
    end_date = fields.Datetime("End Date")
    note = fields.Html('Internal Notes', readonly=True)
    claim_count = fields.Integer(string='# of Claims', compute='_claim_count', readonly=True)
    claim_ids = fields.One2many("hms.insurance.claim", "package_id", string='Claims', copy=False)
    order_line = fields.One2many("hospitalization.package.line", 'order_id', string='Order Lines', readonly=False, copy=True)
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', track_visibility='onchange')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('vehicle.workorder'))
    currency_id = fields.Many2one("res.currency", related='company_id.currency_id', string="Currency", readonly=True, required=True)

    _sql_constraints = [
        ('date_check2', "CHECK (start_date <= end_date)", "The start date must be anterior to the end date."),
    ]

    @api.multi
    def _get_tax_amount_by_group(self):
        self.ensure_one()
        res = {}
        for line in self.order_line:
            base_tax = 0
            for tax in line.tax_id:
                group = tax.tax_group_id
                res.setdefault(group, {'amount': 0.0, 'base': 0.0})
                # FORWARD-PORT UP TO SAAS-17
                price_reduce = line.price_unit * (1.0 - line.discount / 100.0)
                taxes = tax.compute_all(price_reduce + base_tax, quantity=line.product_uom_qty,
                                         product=line.product_id, partner=self.create_uid.partner_id)['taxes']
                for t in taxes:
                    res[group]['amount'] += t['amount']
                    res[group]['base'] += t['base']
                if tax.include_base_amount:
                    base_tax += tax.compute_all(price_reduce + base_tax, quantity=1, product=line.product_id,
                                                partner=self.create_uid.partner_id)['taxes'][0]['amount']
        res = sorted(res.items(), key=lambda l: l[0].sequence)
        res = [(l[0].name, l[1]['amount'], l[1]['base'], len(res)) for l in res]
        return res


class HospitalizationPackageLine(models.Model):
    _name = 'hospitalization.package.line'
    _description = "Package Line"

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.create_uid.partner_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    order_id = fields.Many2one('hospitalization.package', string='Order', required=True, ondelete='cascade', index=True, copy=False)
    name = fields.Text(string='Description', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict', required=True)
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    price_unit = fields.Float()
    discount = fields.Float()
    tax_id = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)])

    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Taxes Amount', readonly=True, store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', readonly=True, store=True)
    currency_id = fields.Many2one(related='order_id.company_id.currency_id', store=True, string='Currency', readonly=True)

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return {'domain': {'product_uom': []}}

        vals = {}
        domain = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = 1.0

        product = self.product_id.with_context(
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            uom=self.product_uom.id
        )

        name = product.name_get()[0][1]
        if product.description_sale:
            name += '\n' + product.description_sale
        vals['price_unit'] = product.lst_price
        vals['name'] = name
        self.update(vals)
        return {'domain': domain}