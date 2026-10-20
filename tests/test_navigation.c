#include "navigation.h"
#include <assert.h>
#include <stdio.h>

int main(void)
{
    assert(navigation_next(PAGE_HOME, INPUT_DOWN) == PAGE_WECHAT);
    assert(navigation_next(PAGE_WECHAT, INPUT_DOWN) == PAGE_HOME);
    assert(navigation_next(PAGE_HOME, INPUT_UP) == PAGE_WECHAT);
    assert(navigation_next(PAGE_WECHAT, INPUT_UP) == PAGE_HOME);
    assert(navigation_next(PAGE_HOME, INPUT_BACK) == PAGE_SETTINGS);
    assert(navigation_next(PAGE_WECHAT, INPUT_BACK) == PAGE_HOME);
    assert(navigation_next(PAGE_SETTINGS, INPUT_BACK) == PAGE_HOME);
    for (int page = 0; page < PAGE_COUNT; ++page)
        assert(navigation_next((page_t)page, INPUT_OK) == (page_t)page);
    assert(navigation_next(PAGE_SETTINGS, INPUT_DOWN) == PAGE_SETTINGS);
    assert(navigation_next(PAGE_SETTINGS, INPUT_UP) == PAGE_SETTINGS);
    assert(navigation_next((page_t)99, INPUT_DOWN) == PAGE_WECHAT);
    puts("Navigation: PASS (two-page carousel, settings entry/exit)");
    return 0;
}
