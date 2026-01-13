#pragma once

/// A singleton for setting and changing global settings.

class Settings {
   public:
    static Settings& instance() {
        static Settings s;
        return s;
    }
    Settings(const Settings&) = delete;
    Settings& operator=(const Settings&) = delete;

    enum class RunType { Test, Scrimmage, Match, InvalidCount };
    enum class SkillsType { None, Driver, Autonomous, InvalidCount };
    enum class FieldQuadrant {
        RedUpper,
        RedLower,
        BlueUpper,
        BlueLower,
        InvalidCount
    };

    RunType run_type{RunType::Test};
    SkillsType skills_type{SkillsType::None};
    FieldQuadrant field_quadrant{FieldQuadrant::RedUpper};

    bool try_win_point{false};
    bool use_experimental_code{false};

   private:
    Settings() = default;
};
