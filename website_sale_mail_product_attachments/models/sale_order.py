# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_current_order_lines_attachments(self):
        attachments_list = []
        for rec in self:
            lines = rec.order_line
            product_template_list = [
                line.product_template_id.id for line in lines]
            product_list = [line.product_id.id for line in lines]
            attachments = self.env['ir.attachment'].search([
                '|',
                '&', '&', ('res_model', '=', 'product.template'), ('res_id', 'in',
                                                                   product_template_list), ('product_downloadable', '=', True),
                '&', '&', ('res_model', '=', 'product.product'), ('res_id', 'in', product_list), ('product_downloadable', '=', True)])
            attachments_list.append(attachments.ids)
        return attachments

    def message_post_with_template(self, template_id, email_layout_xmlid=None, auto_commit=False, **kwargs):
        """ Helper method to send a mail with a template
            :param template_id : the id of the template to render to create the body of the message
            :param **kwargs : parameter to create a mail.compose.message woaerd (which inherit from mail.message)
        """
        # Get composition mode, or force it according to the number of record in self
        if not kwargs.get('composition_mode'):
            kwargs['composition_mode'] = 'comment' if len(
                self.ids) == 1 else 'mass_mail'
        if not kwargs.get('message_type'):
            kwargs['message_type'] = 'notification'
        res_id = kwargs.get('res_id', self.ids and self.ids[0] or 0)
        res_ids = kwargs.get('res_id') and [kwargs['res_id']] or self.ids

        # Create the composer
        composer = self.env['mail.compose.message'].with_context(
            active_id=res_id,
            active_ids=res_ids,
            active_model=kwargs.get('model', self._name),
            default_composition_mode=kwargs['composition_mode'],
            default_email_layout_xmlid=email_layout_xmlid,
            default_model=kwargs.get('model', self._name),
            default_res_id=res_id,
            default_template_id=template_id,
        ).create(kwargs)
        # Simulate the onchange (like trigger in form the view) only
        # when having a template in single-email mode
        if template_id:
            update_values = composer._onchange_template_id(
                template_id, kwargs['composition_mode'], self._name, res_id)['value']
            composer.write(update_values)
        attachment_ids = kwargs.get('attachment_ids')
        if attachment_ids:
            composer.write({'attachment_ids': attachment_ids})
        return composer._action_send_mail(auto_commit=auto_commit)

    def _get_confirmation_template(self):
        ffvoile_template = self.env.ref(
            'ffvoile_sale_product_report.mail_template_option_confirmation_ffvoile', raise_if_not_found=False)
        return ffvoile_template if ffvoile_template else super(SaleOrder, self)._get_confirmation_template()

    def _send_order_confirmation_mail(self):
        if not self:
            return

        if self.env.su:
            self = self.with_user(SUPERUSER_ID)

        for sale_order in self:
            mail_template = sale_order._get_confirmation_template()
            if not mail_template:
                continue

            # Fetch attachments
            attachments = sale_order._get_current_order_lines_attachments()

            # Add attachments to the email
            mail_values = {
                'attachment_ids': [(4, attachment.id) for attachment in attachments]
            }

            sale_order.with_context(force_send=True).message_post_with_template(
                mail_template.id,
                composition_mode='comment',
                email_layout_xmlid='mail.mail_notification_layout_with_responsible_signature',
                **mail_values,
            )
