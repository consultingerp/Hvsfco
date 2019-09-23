# -*- coding: utf-8 -*-
#╔══════════════════════════════════════════════════════════════════╗
#║                                                                  ║
#║                ╔═══╦╗       ╔╗  ╔╗     ╔═══╦═══╗                 ║
#║                ║╔═╗║║       ║║ ╔╝╚╗    ║╔═╗║╔═╗║                 ║
#║                ║║ ║║║╔╗╔╦╦══╣╚═╬╗╔╬╗ ╔╗║║ ╚╣╚══╗                 ║
#║                ║╚═╝║║║╚╝╠╣╔╗║╔╗║║║║║ ║║║║ ╔╬══╗║                 ║
#║                ║╔═╗║╚╣║║║║╚╝║║║║║╚╣╚═╝║║╚═╝║╚═╝║                 ║
#║                ╚╝ ╚╩═╩╩╩╩╩═╗╠╝╚╝╚═╩═╗╔╝╚═══╩═══╝                 ║
#║                          ╔═╝║     ╔═╝║                           ║
#║                          ╚══╝     ╚══╝                           ║
#║ SOFTWARE DEVELOPED AND SUPPORTED BY ALMIGHTY CONSULTING SERVICES ║
#║                   COPYRIGHT (C) 2016 - TODAY                     ║
#║                   http://www.almightycs.com                      ║
#║                                                                  ║
#╚══════════════════════════════════════════════════════════════════╝
{
    'name': 'Hospital Management System Premium',
    'summary': 'Hospital Management System having all modules',
    'description': """
        Hospital Management System Premium. acs hms hospital management system by almighty consulting services.
        hospital certificate and medical crtification medicla dosument management hospital barcode system insurance management system
        laboratory management systemradio logy and pathology management next patient screen,
    """,
    'version': '1.0.2',
    'category': 'Medical',
    'author': 'Almighty Consulting Services',
    'support': 'info@almightycs.com',
    'website': 'https://www.almightycs.com',
    'license': 'OPL-1',
    'depends': [
        'acs_hms', 
        'acs_hms_barcode', 
        'acs_hms_certification',
        'acs_hms_dashboard',
        'acs_hms_hospitalization',
        'acs_hms_document',
        'acs_hms_insurance',
        'acs_hms_laboratory',
        'acs_hms_medical_representative',
        'acs_hms_next_patient_screen',
        'acs_hms_pharmacy',
        'acs_hms_vaccination',
        'acs_hms_portal',
        'acs_hms_commission',
        'facility_management',
        'acs_hms_online_appointment',
        'acs_hms_document_preview',
        'acs_hms_laboratory_preview',
        'acs_hms_operation_theater',
        'acs_hms_icd10',
    ],
    'data': [
    ],
    'images': [
        'static/description/hms_almightycs_cover.jpg',
    ],
    'installable': True,
    'application': True,
    'sequence': 1,
    'price': 0,
    'currency': 'EUR',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: