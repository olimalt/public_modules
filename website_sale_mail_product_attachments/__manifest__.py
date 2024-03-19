# -*- coding: utf-8 -*-
#############################################################################
#
#    Olimalt CHAHIDOV
#
#    Copyright (C) 2024-TODAY Olimalt CHAHIDOV (<https://https://olimalt-chahidov.odoo.com/>)
#    Author: Olimalt CHAHIDOV (<https://https://olimalt-chahidov.odoo.com/>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    "name": "Website order send attachments by mail",
    "summary": "When customer confirm order from the online shop, it sends the attachments of each product to the customer in the confirmation mail.",
    "version": "16.0.1.0.0",
    "category": 'Sales',
    "website": "https://www.olimalt-chahidov.odoo.com",
    "description": """When customer confirm order from the online shop, it sends the attachments of each product to the customer in the confirmation mail.""",
    'author': 'Olimalt CHAHIDOV',
    'company': 'Olimalt CHAHIDOV',
    'maintainer': 'Olimalt CHAHIDOV',
    "depends": [
        'sale_management',
        'website_sale_digital',
    ],
    "data": [],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
