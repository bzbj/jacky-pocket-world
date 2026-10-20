#include "navigation.h"

page_t navigation_next(page_t page, input_t input)
{
    if ((unsigned)page >= PAGE_COUNT) page = PAGE_HOME;
    if (input == INPUT_BACK) return page == PAGE_HOME ? PAGE_SETTINGS : PAGE_HOME;
    if (page == PAGE_SETTINGS || input == INPUT_OK) return page;
    if (input == INPUT_UP || input == INPUT_DOWN)
        return page == PAGE_HOME ? PAGE_WECHAT : PAGE_HOME;
    return page;
}
