#pragma once

#include "utils/settings.hpp"

class PreMatchScreen {
   public:
    PreMatchScreen(Settings& settings) : settings_{settings} {}

    void show();

   private:
    Settings& settings_;
};
