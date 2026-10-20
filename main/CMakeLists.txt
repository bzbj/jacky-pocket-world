idf_component_register(
    SRCS "main.c" "navigation.c" "../assets/screens.c"
    INCLUDE_DIRS "." "../assets"
    REQUIRES bsp esp_timer
)
target_compile_definitions(${COMPONENT_LIB} PRIVATE LV_LVGL_H_INCLUDE_SIMPLE)
