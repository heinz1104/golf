import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {

    async validateOrder(isForceValidate) {
        const currentOrder = this.currentOrder;

        if (currentOrder.config.module_pos_restaurant && currentOrder.preparation_status !== 'ready') {
            this.env.services.notification.add(
                { type: "danger" }
            );
            return;
        }
        await super.validateOrder(...arguments);
    }
});