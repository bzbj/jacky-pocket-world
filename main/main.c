#include "bsp_i2c.h"
#include "bsp_display.h"
#include "bsp_button.h"
#include "bsp_battery.h"
#include "navigation.h"
#include "screens.h"
#include "lvgl.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "freertos/task.h"

static const char *TAG = "pocket_static";
static QueueHandle_t s_inputs;
static lv_obj_t *s_picture, *s_battery;
static page_t s_page = PAGE_HOME;

/* Only runs under the BSP LVGL lock. Reuse objects; no page teardown races. */
static void show_page(page_t page)
{
    static const lv_image_dsc_t *const images[] = {
        &screen_home, &screen_wechat, &screen_settings
    };
    s_page = page;
    lv_image_set_src(s_picture, images[page]);
    ESP_LOGI(TAG, "Static page: %d", (int)page);
}

/* Shared timer callback: queue the action without rendering or I/O. */
static void on_key(bsp_btn_t button, bsp_btn_ev_t event, void *user)
{
    (void)user;
    if (!s_inputs) return;
    input_t input;
    if (event == BSP_BTN_LONG && button == BSP_BTN_OK) input = INPUT_BACK;
    else if (event == BSP_BTN_CLICK && button == BSP_BTN_UP) input = INPUT_UP;
    else if (event == BSP_BTN_CLICK && button == BSP_BTN_DOWN) input = INPUT_DOWN;
    else if (event == BSP_BTN_CLICK && button == BSP_BTN_OK) input = INPUT_OK;
    else return;
    (void)xQueueSend(s_inputs, &input, 0);
}

void app_main(void)
{
    ESP_LOGI(TAG, "Jacky's Pocket World - public static edition");
    if (bsp_i2c_init() != ESP_OK || bsp_display_init() != ESP_OK || !bsp_lvgl_init()) {
        ESP_LOGE(TAG, "Display initialization failed");
        return;
    }
    bool battery_ready = bsp_battery_init() == ESP_OK;
    if (!bsp_lvgl_lock(1000)) {
        ESP_LOGE(TAG, "Display lock timed out");
        return;
    }
    lv_obj_t *screen = lv_obj_create(NULL);
    lv_obj_remove_style_all(screen);
    lv_obj_set_size(screen, 240, 320);
    lv_obj_set_style_bg_color(screen, lv_color_black(), 0);
    lv_obj_set_style_bg_opa(screen, LV_OPA_COVER, 0);
    lv_obj_remove_flag(screen, LV_OBJ_FLAG_SCROLLABLE);
    s_picture = lv_image_create(screen);
    lv_obj_set_pos(s_picture, 0, 0);
    s_battery = lv_label_create(screen);
    lv_obj_set_pos(s_battery, 183, 10);
    lv_obj_set_width(s_battery, 33);
    lv_obj_set_style_text_font(s_battery, &lv_font_montserrat_10, 0);
    lv_obj_set_style_text_color(s_battery, lv_color_hex(0x25465b), 0);
    lv_obj_set_style_text_align(s_battery, LV_TEXT_ALIGN_RIGHT, 0);
    lv_label_set_text(s_battery, "");
    show_page(PAGE_HOME);
    lv_screen_load(screen);
    bsp_lvgl_unlock();
    bsp_display_backlight(100);

    s_inputs = xQueueCreate(8, sizeof(input_t));
    if (!s_inputs) {
        ESP_LOGE(TAG, "Input queue allocation failed");
        return;
    }
    if (bsp_button_init(on_key, NULL) != ESP_OK) {
        ESP_LOGE(TAG, "Buttons unavailable; home remains visible");
        vQueueDelete(s_inputs);
        s_inputs = NULL;
        return;
    }
    int64_t last_battery = -30000;
    for (;;) {
        input_t input;
        if (xQueueReceive(s_inputs, &input, pdMS_TO_TICKS(250)) == pdTRUE) {
            page_t next = navigation_next(s_page, input);
            if (next != s_page && bsp_lvgl_lock(500)) {
                show_page(next);
                bsp_lvgl_unlock();
            }
        }
        int64_t now = esp_timer_get_time() / 1000;
        if (now - last_battery >= 30000) {
            int percent = battery_ready ? bsp_battery_soc() : -1;
            if (bsp_lvgl_lock(250)) {
                if (percent >= 0 && percent <= 100)
                    lv_label_set_text_fmt(s_battery, "%d%%", percent);
                else lv_label_set_text(s_battery, "");
                bsp_lvgl_unlock();
            }
            last_battery = now;
        }
    }
}
