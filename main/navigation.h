#pragma once

typedef enum { PAGE_HOME, PAGE_WECHAT, PAGE_SETTINGS, PAGE_COUNT } page_t;
typedef enum { INPUT_UP, INPUT_DOWN, INPUT_OK, INPUT_BACK } input_t;

/* Settings is a static showcase. Only home/wechat are in the carousel. */
page_t navigation_next(page_t page, input_t input);
