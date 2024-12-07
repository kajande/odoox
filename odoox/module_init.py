from pathlib import Path

def get_manifest_file(name):
    # Create __manifest__.py
    module_dir = Path(name)
    manifest_file = module_dir / '__manifest__.py'
    manifest_file.write_text(
        f"""# -*- coding: utf-8 -*-
{{
    'name': '{name.capitalize()}',
    'version': '17.0',
    'category': 'Custom',
    'summary': 'A custom module for Odoo',
    'description': 'Description of {name.capitalize()} module.',
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'depends': ['base', 'module11'],
    'data': [
        'security/ir.model.access.csv',
        'views/{name}_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}}
"""
    )

def get_init_file(name):
    # Create __init__.py for the module
    module_dir = Path(name)
    init_file = module_dir / '__init__.py'
    init_file.write_text(f"from . import models\n")


def get_gitx(name):
    # Create the gitx.conf file
    module_dir = Path(name)
    gitx_file = module_dir / 'gitx.conf'
    gitx_file.write_text(
    """[module11]
pulluri = https://github.com/odoox-demo-org/repo1.git
branch =
track =
"""
    )

def get_security(name):
    module_dir = Path(name)
    security_dir = module_dir / 'security'
    security_dir.mkdir(exist_ok=True)

    access_file = security_dir / 'ir.model.access.csv'
    access_file.write_text(
        f"""id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_{name}_all,{name.capitalize()} Access,model_{name},base.group_user,1,1,1,1
"""
    )

def get_models_dir(name):
    # Create security directory and ir.model.access.csv
    module_dir = Path(name)
    models_dir = module_dir / 'models'
    models_dir.mkdir(exist_ok=True)

    models_init_file = models_dir / '__init__.py'
    models_init_file.write_text(f"from . import {name}\n")

    # Create a sample model
    model_file = models_dir / f"{name}.py"
    model_file.write_text(
        f"""# -*- coding: utf-8 -*-
from odoo import models, fields

class {name.capitalize()}(models.Model):
    _name = '{name}'
    _description = '{name.capitalize()} Model'

    name = fields.Char(string="Name", required=True)
"""
    )

def get_views_dir(name):
    # Create views directory and XML file
    module_dir = Path(name)
    views_dir = module_dir / 'views'
    views_dir.mkdir(exist_ok=True)

    views_file = views_dir / f'{name}_views.xml'
    views_file.write_text(
        f"""<odoo>
    <!-- Tree View -->
    <record id="view_{name}_tree" model="ir.ui.view">
        <field name="name">{name}.tree</field>
        <field name="model">{name}</field>
        <field name="arch" type="xml">
            <tree string="{name.capitalize()}">
                <field name="name"/>
            </tree>
        </field>
    </record>

    <!-- Form View -->
    <record id="view_{name}_form" model="ir.ui.view">
        <field name="name">{name}.form</field>
        <field name="model">{name}</field>
        <field name="arch" type="xml">
            <form string="{name.capitalize()}">
                <sheet>
                    <group>
                        <field name="name"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Action -->
    <record id="action_{name}" model="ir.actions.act_window">
        <field name="name">{name.capitalize()}s</field>
        <field name="res_model">{name}</field>
        <field name="view_mode">tree,form</field>
    </record>

    <!-- Menu Items -->
    <menuitem id="menu_{name}" name="{name.capitalize()}" sequence="1"/>
    <menuitem id="menu_{name}_main" name="{name.capitalize()}s" parent="menu_{name}" action="action_{name}"/>
</odoo>
"""
    )
