/** @odoo-module **/
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { _t } from "@web/core/l10n/translation";
import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";

class CustomControlButton extends ProductScreen {
    static template = "CustomControlButton";
    async onClick() {
        const { confirmed } = await this.popup.add(ConfirmPopup, {
            title: _t("Popup"),
            body: _t("Custom control button was clicked"),
            confirmText: _t("Ok"),
            cancelText: _t("Close"),
        });
    }
}
ProductScreen.addControlButton({
    component: CustomControlButton,
    position: ['after', 'OrderlineCustomerNoteButton'],
});
