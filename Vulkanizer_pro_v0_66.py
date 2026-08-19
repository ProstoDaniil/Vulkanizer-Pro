# -*- coding: utf-8 -*-
"""
==============================================================================
  ВУЛКАНИЗАТОР ПРО альфа v0.66 (ИНТЕЛЛЕКТУАЛЬНЫЙ ОПТИМИЗАТОР & ВРАППЕР) - GUI EDITION
  ДЛЯ ИСТИННЫХ ГЕЙМЕРОВ. ОТ ТЕХ, КТО В ИГРЕ! | FOR TRUE GAMERS. BY THOSE WHO PLAY!
==============================================================================
"""

import os
import sys
import re
import json
import shutil
import ctypes
import tempfile
import threading
import subprocess
import urllib.request
import tarfile
import fnmatch
import webbrowser
from pathlib import Path

try:
    import winreg
except ImportError:
    winreg = None

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

LOCALIZATION = {
    'RUS': {
        'title': "ВУЛКАНИЗАТОР ПРО v0.66",
        'subtitle': "Интеллектуальный оптимизатор & враппер",
        'motto': "ДЛЯ ИСТИННЫХ ГЕЙМЕРОВ. ОТ ТЕХ, КТО В ИГРЕ!",
        'tab_games': "ИГРЫ И НАСТРОЙКИ",
        'tab_tweaks': "ГЛОБАЛЬНЫЕ ТВИКИ",
        'tab_console': "КОНСОЛЬ & ЛОГИ",
        'tab_about': "О ПРОГРАММЕ",
        'admin_required': "ВНИМАНИЕ: Требуются права Администратора!",
        'admin_desc': "Для изменения глубоких системных параметров реестра, сетевого стека и схем электропитания запустите приложение от имени Администратора.",
        'btn_elevate': "Запустить как Администратор",
        'disclaimer_title': "⚠️ ДИСКЛЕЙМЕР И МЕДВЕДИ",
        'disclaimer_text': (
            "Этот скрипт делает бэкапы и вряд ли что-то сломает. Вы всегда можете всё восстановить.\n\n"
            "НО ПОМНИТЕ: Не на всех конфигурациях все игры будут работать! Всё зависит от вашего железа "
            "и кривизны рук разработчиков.\n\n"
            "Совет: Для максимальной стабильности с Vulkan запускайте игры в режиме 'Окно без рамки' "
            "(Borderless Windowed). Это предотвращает вылеты при сворачивании (Alt+Tab), убирает "
            "задержки ввода и гарантирует стабильную работу оверлеев.\n\n"
            "ОБЯЗАТЕЛЬНО: В наших пресетах вертикальная синхронизация ВКЛЮЧЕНА ПО УМОЛЧАНИЮ "
            "(через DXVK). Чтобы получить максимум, снизить лаг и избежать двойной синхронизации — "
            "ВЫКЛЮЧИТЕ V-Sync В НАСТРОЙКАХ САМОЙ ИГРЫ!\n\n"
            "🚨 ВАЖНО ДЛЯ ИГР UBISOFT (Assassin's Creed, Watch Dogs и др.):\n"
            "Если вы устанавливаете Вулканизатор на игры Ubisoft, обязательно выполните следующие шаги:\n"
            "  1. Откройте лаунчер Ubisoft Connect.\n"
            "  2. Перейдите в Меню -> Настройки -> вкладка 'Интерфейс'.\n"
            "  3. Снимите галочку с пункта 'Включить внутриигровой оверлей для поддерживаемых игр'.\n"
            "  4. Запускайте игру СТРОГО через сам лаунчер Ubisoft Connect, а не напрямую через EXE!\n"
            "Оверлей Ubisoft часто вызывает моментальные краши при работе с Vulkan API.\n\n"
            "Также помните: вероятность встретить медведя с дробовиком крайне мала, но никогда не равна нулю!"
        ),
        'accept_risks': "Я принимаю риски, продолжить",
        'btn_scan_steam': "Сканировать Steam",
        'btn_add_folder': "Добавить папку игры",
        'btn_add_file': "Добавить EXE-файл",
        'no_games': "Игры не найдены. Запустите сканирование или добавьте путь вручную.",
        'analyzing_api': "Анализ API...",
        'game_settings_for': "Настройки для: {}",
        'select_preset': "Выберите пресет оптимизации:",
        'preset_cinematic': "🎬 Синематик Ультра",
        'preset_cinematic_desc': "Максимальная плавность, 4 буфера, ультра детализация, SRS-like резкость, LOD -2.0.",
        'preset_ultra': "🔥 Ультра качество",
        'preset_ultra_desc': "Высокое качество, низкая задержка, анизотропная фильтрация 16x, LOD -1.0.",
        'preset_best': "✨ Лучшая картинка",
        'preset_best_desc': "Четкость и плавность, приоритет FPS, LOD -0.5, анизотропная фильтрация 16x.",
        'preset_balance': "⚖️ Сбалансированный",
        'preset_balance_desc': "Оптимальное соотношение качества и производительности, анизотропия 8x.",
        'preset_vanilla': "🧊 Чистый Vulkan",
        'preset_vanilla_desc': "Чистый DXVK + высокий приоритет CPU + низкая задержка кадров, без твиков графики.",
        'install_vulkanizer': "🚀 УСТАНОВИТЬ ВУЛКАНИЗАТОР",
        'vsync_buffering': "Синхронизация и Буферизация:",
        'vsync_on': "V-Sync: ВКЛ (Рекомендуется)",
        'vsync_off': "V-Sync: ВЫКЛ (Мин. задержка)",
        'vsync_half': "V-Sync: ПОЛОВИННЫЙ x2",
        'buffering_double': "Двойная буферизация (2 кадра)",
        'buffering_triple': "Тройная буферизация (3 кадра)",
        'buffering_quad': "Квадро буферизация (4 кадра)",
        'overlay_mgmt': "Оверлей и Мониторинг:",
        'overlay_none': "Без оверлея",
        'overlay_fps': "Минимальный (только FPS)",
        'overlay_extended': "Расширенный мониторинг",
        'overlay_full': "Полная диагностика (Всё + графики)",
        'maintenance_tools': "Инструменты обслуживания:",
        'btn_clean_cache': "🧹 Очистить кэш игры",
        'btn_reset_settings': "🔄 Сбросить настройки игры",
        'btn_deep_uninstall': "❌ Удалить Вулканизатор",
        'btn_desktop_shortcut': "🔗 Создать ярлык",
        'btn_launch_game': "🚀 Запустить игру",
        'log_level': "Логирование DXVK:",
        'log_enabled': "Включить создание .log файлов",
        'log_disabled': "Отключить создание .log файлов",
        'spoof_vram': "🔧 Ультимативный Фикс GTA 4: Эмуляция топ-видеокарты GTX 680 (Разблок памяти)",
        'btn_on': "ВКЛ",
        'btn_off': "ВЫКЛ",
        'api_override_title': "Принудительный выбор API (Оверрайд):",
        'global_tweaks_desc': "Глобальные оптимизации операционной системы для экстремальной производительности.",
        'tweak_cache_title': "1. ОПТИМИЗАЦИЯ: Единый глобальный кэш DXVK",
        'tweak_cache_desc': "Оптимизирует кэширование шейдеров, перенося файлы *.dxvk-cache всех игр в единую папку C:\\DXVK_Cache. Предотвращает статтеры, ускоряет загрузку графики.",
        'tweak_gamemode_title': "2. ОПТИМИЗАЦИЯ: Игровой режим Windows (Game Mode)",
        'tweak_gamemode_desc': "Оптимизирует приоритеты ресурсов CPU/GPU под запущенный игровой процесс, полностью подавляя фоновые задачи системы и Центра обновления.",
        'tweak_gamedvr_title': "3. ОПТИМИЗАЦИЯ: Отключение Xbox GameDVR",
        'tweak_gamedvr_desc': "Оптимизирует дисковую подсистему и CPU путем отключения фоновой циклической записи экрана, которая создает скрытую паразитную нагрузку и снижает FPS.",
        'tweak_gpucache_title': "4. ОПТИМИЗАЦИЯ: Очистка кэша драйвера GPU",
        'tweak_gpucache_desc': "Оптимизирует стабильность видеочипа, проводя глубокую очистку старых, фрагментированных и битых шейдеров в системных папках NVIDIA / AMD.",
        'tweak_power_title': "5. ОПТИМИЗАЦИЯ: Схема питания 'Максимальная производительность'",
        'tweak_power_desc': "Оптимизирует энергопитание железа: активирует схему 'Ultimate Performance', запрещает парковку ядер CPU, засыпание накопителей, а также полностью блокирует автоматическое гашение экрана и переход компьютера в спящий режим/выключение при простое.",
        'tweak_prio_title': "6. ОПТИМИЗАЦИЯ: Приоритеты планировщика CPU",
        'tweak_prio_desc': "Оптимизирует кванты времени процессора (Win32PrioritySeparation), выделяя максимальный неделимый ресурс активному игровому окну для ровного фреймтайма.",
        'tweak_hags_title': "7. ОПТИМИЗАЦИЯ: Аппаратное планирование GPU (HAGS)",
        'tweak_hags_desc': "Оптимизирует видеопамять, делегируя управление текстурами напрямую контроллеру видеокарты в обход драйвера ОС. Значительно снижает инпут-лаг.",
        'tweak_network_title': "8. ОПТИМИЗАЦИЯ: Сетевой стек и низкий пинг (MMSS)",
        'tweak_network_desc': "Оптимизирует передачу пакетов (отключает лимитирование сети для снижения пинга) и выделяет игре 100% процессорных ресурсов планировщика мультимедиа MMCSS.",
        'tweak_nagle_title': "9. ОПТИМИЗАЦИЯ: Игровой пинг и алгоритм Нагла",
        'tweak_nagle_desc': "Оптимизирует сетевые задержки (TcpAckFrequency/TcpNoDelay), полностью отключая буферизацию пакетов Windows. Отправляет данные мгновенно, снижая пинг в онлайн-матчах.",
        'tweak_faststart_title': "10. ОПТИМИЗАЦИЯ: Чистое завершение работы Windows",
        'tweak_faststart_desc': "Оптимизирует запуск системы путем отключения Fast Startup. Заставляет ПК выключаться полностью, очищая ОЗУ от накопленных багов и утечек памяти.",
        'tweak_hpet_title': "11. ОПТИМИЗАЦИЯ: Отключение HPET и тиков таймера",
        'tweak_hpet_desc': "Оптимизирует задержки: отключает HPET и Dynamic Tick, запрещая процессору уходить в микро-сон в игровом процессе. Убирает фризы при резких движениях мыши.",
        'tweak_tempclean_title': "12. ОПТИМИЗАЦИЯ: Очистка временных файлов диска",
        'tweak_tempclean_desc': "Оптимизирует свободное место и нагрузку на SSD/HDD, проводя глубокую очистку каталогов Windows Temp и Prefetch от накопленного системного мусора.",
        'tweak_aero_title': "13. ОПТИМИЗАЦИЯ: Отключение прозрачности Windows",
        'tweak_aero_desc': "Оптимизирует производительность видеокарты, отключая эффекты прозрачности Aero/Fluent. Освобождает ресурсы GPU для рендеринга игры, повышая стабильный FPS.",
        'btn_reset_all_tweaks': "🚨 СБРОСИТЬ ВСЕ ГЛОБАЛЬНЫЕ ТВИКИ К ДЕФОЛТУ",
        'about_text': (
            "ВУЛКАНИЗАТОР ПРО — это удобный графический враппер и оптимизатор.\n\n"
            "Этот проект НЕ является заменой или альтернативой оригинальному DXVK.\n"
            "Мы глубоко уважаем и ценим титанический труд Филиппа Ребо (doitsujin) "
            "и всей команды оригинального DXVK за революцию в трансляции вызовов "
            "DirectX 9/10/11 в Vulkan API!\n\n"
            "Наша утилита автоматизирует рутину: скачивает оригинальные библиотеки "
            "с GitHub, распределяет их, разблокирует в Windows, настраивает профили "
            "совместимости и применяет проверенные игровые твики ОС.\n\n"
            "Официальный репозиторий DXVK: https://github.com/doitsujin/dxvk\n\n"
            "Создатели враппера: EvilCat & AI (Золотой Стандарт)\n"
            "Контакты создателя: Telegram @EvilCat_97\n"
            "Модификация, улучшение и адаптация: Звёздочка\n"
            "Специально для: Для геймеров"
        ),
        'status_active': "🟢 АКТИВЕН",
        'status_inactive': "🔴 ОТКЛЮЧЕН",
        'status_cleaner': "🧹 ОДНОКРАТНО",
        'status_not_optimized': "🟡 НЕ ОПТИМИЗИРОВАН",
        'status_ready': "🟢 Готов к работе",
        'status_downloading': "⏳ Скачивание DXVK с GitHub ({:.1f}%)...",
        'status_extracting': "⏳ Распаковка файлов...",
        'status_install_success': "✅ Вулканизатор успешно установлен в {}!",
        'status_uninstall_success': "✅ Вулканизатор полностью удален из {}!",
        'status_cache_clean_success': "🧹 Кэш шейдеров успешно очищен!",
        'status_profile_reset_success': "🔄 Настройки профиля игры сброшены!",
        'tweak_applied': "✅ Твик успешно применен!",
        'tweak_disabled': "❌ Твик отключен/сброшен!",
        'tweak_btn_enable': "ВКЛЮЧИТЬ",
        'tweak_btn_disable': "ОТКЛЮЧИТЬ",
        'tweak_btn_clear': "ОЧИСТИТЬ",
        'dxvk_version_title': "Версия транслятора DXVK:",
        'dxvk_latest': "Новейшая версия (v2.4+ / Vulkan 1.3)",
        'dxvk_legacy': "Legacy-совместимая (v1.10.3 / Vulkan 1.1)",
        'search_placeholder': "🔍 Поиск по названию игры или EXE...",
        'tooltip_folder': "Выбрать корневую ПАПКУ игры для сканирования и установки",
        'tooltip_file': "Выбрать конкретный исполняемый EXE-файл игры напрямую"
    },
    'ENG': {
        'title': "VULKANIZER PRO v0.66",
        'subtitle': "Intelligent Optimizer & Service Wrapper",
        'motto': "FOR TRUE GAMERS. BY THOSE WHO PLAY!",
        'tab_games': "GAMES & SETTINGS",
        'tab_tweaks': "GLOBAL SYSTEM TWEAKS",
        'tab_console': "CONSOLE & LOGS",
        'tab_about': "ABOUT",
        'admin_required': "WARNING: Administrator Rights Required!",
        'admin_desc': "To modify deep registry keys, network stack behaviors, and performance power plans, please run this application as Administrator.",
        'btn_elevate': "Run as Administrator",
        'disclaimer_title': "⚠️ DISCLAIMER & BEARS WITH SHOTGUNS",
        'disclaimer_text': (
            "This script makes backups and is highly unlikely to break anything. You can always restore your settings.\n\n"
            "BUT REMEMBER: Not all games will run on all configurations! It entirely depends on your hardware "
            "and the game developers' crooked hands.\n\n"
            "Tip: For maximum stability with Vulkan, run games in 'Borderless Windowed' mode. This prevents "
            "Alt+Tab crashes, eliminates frame latency spikes, and ensures stable overlay operation.\n\n"
            "MANDATORY: Our presets have vertical synchronization ENABLED BY DEFAULT "
            "(via DXVK). To get the most out of your game and avoid double synchronization lag, "
            "DISABLE V-Sync IN THE GAME'S OWN SETTINGS!\n\n"
            "🚨 CRITICAL FOR UBISOFT GAMES (Assassin's Creed, Watch Dogs, etc.):\n"
            "If you install Vulkanizer on Ubisoft titles, follow these steps strictly:\n"
            "  1. Open the Ubisoft Connect desktop application.\n"
            "  2. Navigate to Menu -> Settings -> 'Interface' tab.\n"
            "  3. Uncheck 'Enable in-game overlay for supported games'.\n"
            "  4. Always launch the game DIRECTLY from the Ubisoft Connect library, NOT the raw EXE!\n"
            "The Ubisoft overlay is prone to instant crashes when translation layers are active.\n\n"
            "Also remember: the chances of encountering a bear with a shotgun are extremely low, but never zero!"
        ),
        'accept_risks': "I accept the risks, let's begin",
        'btn_scan_steam': "Scan Steam Library",
        'btn_add_folder': "Add Game Folder",
        'btn_add_file': "Add Game EXE File",
        'no_games': "No games found. Start scanning or add a path manually.",
        'analyzing_api': "Analyzing API...",
        'game_settings_for': "Settings for: {}",
        'select_preset': "Select Optimization Preset:",
        'preset_cinematic': "🎬 Cinematic Ultra",
        'preset_cinematic_desc': "Ultimate smoothness, 4 buffers, ultra detail levels, SRS-like sharpening, LOD -2.0.",
        'preset_ultra': "🔥 Ultra Quality",
        'preset_ultra_desc': "High visual quality, low latency settings, 16x anisotropic filtering, LOD -1.0.",
        'preset_best': "✨ Best Picture",
        'preset_best_desc': "Crisp details + high fluidity, FPS priority, LOD -0.5, 16x anisotropic filtering.",
        'preset_balance': "⚖️ Balanced Performance",
        'preset_balance_desc': "Optimized sweet-spot for visual fidelity and FPS, 8x anisotropic filtering.",
        'preset_vanilla': "🧊 Pure Vulkan",
        'preset_vanilla_desc': "Clean DXVK translation layer + high CPU priority + low input lag, no graphics tweaks.",
        'install_vulkanizer': "🚀 INSTALL VULKANIZER",
        'vsync_buffering': "Sync & Frame Buffering:",
        'vsync_on': "V-Sync: ENABLED (Recommended)",
        'vsync_off': "V-Sync: DISABLED (Lowest Latency)",
        'vsync_half': "V-Sync: HALF SPEED x2",
        'buffering_double': "Double Buffering (2 frames)",
        'buffering_triple': "Triple Buffering (3 frames)",
        'buffering_quad': "Quad Buffering (4 frames)",
        'overlay_mgmt': "Overlay & Monitoring Setup:",
        'overlay_none': "Disable Overlay",
        'overlay_fps': "Minimalist (FPS counter only)",
        'overlay_extended': "Extended Frame Analysis",
        'overlay_full': "Full Diagnostic HUD (All details + charts)",
        'maintenance_tools': "Maintenance & Control Toolkit:",
        'btn_clean_cache': "🧹 Clear Game Cache",
        'btn_reset_settings': "🔄 Reset Game Configuration",
        'btn_deep_uninstall': "❌ Deep Uninstall Wrapper",
        'btn_desktop_shortcut': "🔗 Create Desktop Shortcut",
        'btn_launch_game': "🚀 Launch Game Now",
        'log_level': "DXVK Translation Logs:",
        'log_enabled': "Enable game folder .log creation",
        'log_disabled': "Disable game folder .log creation",
        'spoof_vram': "🔧 Ultimate GTA 4 Fix: Emulate GTX 680 (VRAM Unlock)",
        'btn_on': "ON",
        'btn_off': "OFF",
        'api_override_title': "Force API Version (Override):",
        'global_tweaks_desc': "Global operating system optimizations designed to squeeze maximum performance out of your PC.",
        'tweak_cache_title': "1. OPTIMIZATION: Unified Global DXVK Cache",
        'tweak_cache_desc': "Optimizes shader compiling by consolidating all *.dxvk-cache files into C:\\DXVK_Cache. Eliminates micro-stutters and speeds up visuals loading.",
        'tweak_gamemode_title': "2. OPTIMIZATION: Windows Game Mode Integration",
        'tweak_gamemode_desc': "Optimizes resource priorities for CPU and GPU directly to the running game process, suppressing background tasks.",
        'tweak_gamedvr_title': "3. OPTIMIZATION: Disable Xbox GameDVR Service",
        'tweak_gamedvr_desc': "Optimizes disk I/O and CPU overhead by disabling background video recording which constantly consumes gaming FPS.",
        'tweak_gpucache_title': "4. OPTIMIZATION: GPU Driver Shader Cache Cleanup",
        'tweak_gpucache_desc': "Optimizes video chip stability by performing a deep clean of corrupt, old, or legacy driver-level shader caches for NVIDIA & AMD.",
        'tweak_power_title': "5. OPTIMIZATION: Power Plan: Ultimate Performance",
        'tweak_power_desc': "Optimizes hardware power state: activates high-performance scheme, disables core parking, disk standby, and completely prevents display standby and system sleep/hibernation when idling.",
        'tweak_prio_title': "6. OPTIMIZATION: CPU Schedule Priority Optimization",
        'tweak_prio_desc': "Optimizes processor timeslices (Win32PrioritySeparation), forcing the Windows thread scheduler to allocate maximal resources directly to the active game.",
        'tweak_hags_title': "7. OPTIMIZATION: Hardware-Accelerated GPU Scheduling",
        'tweak_hags_desc': "Optimizes video memory management by delegating textures handling directly to the GPU hardware, reducing frame delivery latency.",
        'tweak_network_title': "8. OPTIMIZATION: Network & Scheduler Tweaks (MMSS)",
        'tweak_network_desc': "Optimizes packets delivery (eliminates network throttling for lower ping) and assigns 100% priority in MMCSS to gaming threads.",
        'tweak_nagle_title': "9. OPTIMIZATION: Game Ping & Nagle's Algorithm",
        'tweak_nagle_desc': "Optimizes network latency (TcpAckFrequency/TcpNoDelay) by disabling Windows packet buffering, instantly sending game packets.",
        'tweak_faststart_title': "10. OPTIMIZATION: Disable Windows Fast Startup",
        'tweak_faststart_desc': "Optimizes OS initialization by forcing a genuine clean shutdown when turning off your PC, clearing system RAM leaks.",
        'tweak_hpet_title': "11. OPTIMIZATION: Disable HPET & Dynamic Power Ticks",
        'tweak_hpet_desc': "Optimizes input delay: stops CPU core sleep states during micro-delays, flattening frametime spikes and removing mouse latency.",
        'tweak_tempclean_title': "12. OPTIMIZATION: Clean Temporary Files",
        'tweak_tempclean_desc': "Optimizes SSD/HDD storage capacity and active load by cleaning Windows Temp and Prefetch directories of clutter.",
        'tweak_aero_title': "13. OPTIMIZATION: Disable Transparency",
        'tweak_aero_desc': "Optimizes graphics card overhead by disabling Aero/Fluent transparency effects. Frees up GPU resources directly for game rendering.",
        'btn_reset_all_tweaks': "🚨 RESET ALL GLOBAL SYSTEM TWEAKS TO DEFAULT",
        'about_text': (
            "VULKANIZER PRO is a convenient graphical service wrapper and performance optimizer.\n\n"
            "This project is NOT a replacement or alternative to the original DXVK translation project.\n"
            "We deeply respect and sincerely appreciate the titanic efforts of Philip Rebo (doitsujin) "
            "and the entire original DXVK contributor team for revolutionizing the translation "
            "of DirectX 9/10/11 calls into Vulkan API!\n\n"
            "Our tool simply automates the routine: it retrieves original binaries from the "
            "official repository, organizes them by architecture, unlocks them in Windows, configure "
            "compatibility registry flags, and applies time-tested OS gaming tweaks.\n\n"
            "Official DXVK Repository: https://github.com/doitsujin/dxvk\n\n"
            "Wrapper Creators: EvilCat & AI (Golden Standard)\n"
            "Creator Contacts: Telegram @EvilCat_97\n"
            "Modification & Improvements: Zvezdochka\n"
            "Specially for: For gamers"
        ),
        'status_active': "🟢 ACTIVE",
        'status_inactive': "🔴 INACTIVE",
        'status_cleaner': "🧹 ONE-TIME",
        'status_not_optimized': "🟡 NOT OPTIMIZED",
        'status_ready': "🟢 Ready",
        'status_downloading': "⏳ Downloading latest DXVK ({:.1f}%)...",
        'status_extracting': "⏳ Extracting files...",
        'status_install_success': "✅ Vulkanizer installed successfully in {}!",
        'status_uninstall_success': "✅ Vulkanizer completely removed from {}!",
        'status_cache_clean_success': "🧹 Game state cache cleared successfully!",
        'status_profile_reset_success': "🔄 Game configuration files reset!",
        'tweak_applied': "✅ Tweak applied successfully!",
        'tweak_disabled': "❌ Tweak disabled/reset!",
        'tweak_btn_enable': "ENABLE",
        'tweak_btn_disable': "DISABLE",
        'tweak_btn_clear': "CLEAR",
        'dxvk_version_title': "DXVK Translator Version:",
        'dxvk_latest': "Latest stable (v2.4+ / Vulkan 1.3)",
        'dxvk_legacy': "Legacy compatible (v1.10.3 / Vulkan 1.1)",
        'search_placeholder': "🔍 Search by game name or EXE...",
        'tooltip_folder': "Select game root FOLDER for scanning and installation",
        'tooltip_file': "Select a specific game EXE executable file directly"
    }
}

THEME = {
    'bg_main': "#0d0e12",       # Темный космос
    'bg_sidebar': "#12131a",    # Навигационная панель
    'bg_card': "#181a24",       # Карточки игр и твиков
    'bg_card_sel': "#222533",   # Активный выбор
    'accent_cyan': "#00f0ff",   # Неоновый Циан
    'accent_pink': "#ff007f",   # Неоновый Розовый
    'accent_green': "#39ff14",  # Неоновый Зеленый
    'text_light': "#ffffff",    # Белый текст
    'text_gray': "#8f93a3",     # Серый текст
    'text_dark': "#12131a"      # Контрастный темный
}

class ToolTip:
    """Создает всплывающие подсказки с неоновой границей при наведении мыши."""
    active_tip = None

    def __init__(self, widget, text_func):
        self.widget = widget
        self.text_func = text_func
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)
        self.widget.bind("<ButtonPress>", self.hide_tip)

    def show_tip(self, event=None):
        if ToolTip.active_tip and ToolTip.active_tip != self:
            ToolTip.active_tip.hide_tip()

        if self.tip_window or not self.text_func():
            return
        
        try:
            x = self.widget.winfo_pointerx() + 15
            y = self.widget.winfo_pointery() + 15
        except Exception:
            x = self.widget.winfo_rootx() + 25
            y = self.widget.winfo_rooty() + 35

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        frame = tk.Frame(tw, bg=THEME['accent_cyan'], bd=1)
        frame.pack()
        label = tk.Label(frame, text=self.text_func(), justify=tk.LEFT,
                         background=THEME['bg_sidebar'], foreground=THEME['text_light'],
                         font=("Segoe UI", 9), padx=10, pady=8, wraplength=320)
        label.pack()
        
        ToolTip.active_tip = self

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            try:
                tw.destroy()
            except Exception:
                pass
        if ToolTip.active_tip == self:
            ToolTip.active_tip = None

class VulkanizerModel:
    def __init__(self, console_callback=None):
        self.console_callback = console_callback
        self.temp_dir = Path(tempfile.gettempdir()) / "Vulkanizer"
        self.cpu_cores = os.cpu_count() or 4
        self.gpu_name, self.gpu_vendor = self._get_gpu_info()
        self.games = []
        self._ensure_temp_dir()

    def log(self, message):
        if self.console_callback:
            self.console_callback(f"[SYS] {message}\n")
        else:
            print(f"[SYS] {message}")

    def _ensure_temp_dir(self):
        if not self.temp_dir.exists():
            self.temp_dir.mkdir(parents=True, exist_ok=True)

    def _get_gpu_info(self):
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            result = subprocess.run(
                ["powershell", "-Command", "Get-CimInstance Win32_VideoController | Select-Object -First 1 -ExpandProperty Name"],
                capture_output=True, text=True, startupinfo=startupinfo
            )
            gpu_name = result.stdout.strip() if result.stdout else "Unknown GPU"
        except Exception:
            gpu_name = "Generic GPU"
        
        gpu_vendor = "Generic"
        gpu_name_upper = gpu_name.upper()
        if "NVIDIA" in gpu_name_upper:
            gpu_vendor = "NVIDIA"
        elif "AMD" in gpu_name_upper or "RADEON" in gpu_name_upper:
            gpu_vendor = "AMD"
        elif "INTEL" in gpu_name_upper:
            gpu_vendor = "Intel"
            
        return gpu_name, gpu_vendor

    def check_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    def get_exe_architecture(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                f.seek(0x3C)
                pe_offset = int.from_bytes(f.read(4), 'little')
                f.seek(pe_offset)
                pe_sig = f.read(4)
                if pe_sig == b'PE\x00\x00':
                    machine = int.from_bytes(f.read(2), 'little')
                    if machine == 0x014c:
                        return "x32"
                    elif machine == 0x8664:
                        return "x64"
        except Exception as e:
            self.log(f"Architecture check failed for {filepath}: {e}")
        return "x64"

    def scan_exe_api(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                header = f.read(10 * 1024 * 1024)
                header_str = header.decode('utf-16le', errors='ignore') + header.decode('utf-8', errors='ignore')
                
                if "d3d11.dll" in header_str.lower():
                    return "DX11"
                elif "d3d12.dll" in header_str.lower():
                    return "DX12"
                elif "d3d9.dll" in header_str.lower():
                    return "DX9"
                elif "d3d10core.dll" in header_str.lower() or "d3d10" in header_str.lower():
                    return "DX10"
        except Exception as e:
            self.log(f"API deep analysis failed for {filepath}: {e}")
        return "Unknown"

    def scan_steam_games_iterative(self, progress_callback=None):
        self.log("Starting incremental Steam library scan with restricted folder depth...")
        games_found = []
        if winreg is None:
            return games_found

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
            steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
            winreg.CloseKey(key)
        except Exception as e:
            self.log(f"Steam is not registered: {e}")
            return games_found

        library_vdf = Path(steam_path) / "steamapps" / "libraryfolders.vdf"
        if not library_vdf.exists():
            return games_found

        try:
            with open(library_vdf, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            paths = re.findall(r'"path"\s+"([^"]+)"', content)
            paths = [p.replace('\\\\', '\\') for p in paths]
        except Exception as e:
            self.log(f"Failed to parse libraryfolders.vdf: {e}")
            return games_found

        exclude_dirs = ["*dependencies*", "*repro*", "*shadercache*", "*crashpad*", "*install*", "*overlay*", "*_CommonRedist*", "*vcredist*", "*DirectX*", "*DotNet*", "*redist*"]
        exclude_files = ["*unins*", "*setup*", "*crash*", "*update*", "*redist*", "*dxsetup*", "*webhelper*", "*reporter*", "*install*", "*launcher_cef*", "*vcredist*", "*Subprocess*"]

        game_directories = []
        for path in paths:
            common_dir = Path(path) / "steamapps" / "common"
            if common_dir.exists():
                try:
                    for entry in os.scandir(common_dir):
                        if entry.is_dir():
                            game_directories.append(Path(entry.path))
                except Exception:
                    pass

        total_dirs = len(game_directories)
        if total_dirs == 0:
            return games_found

        for idx, g_dir in enumerate(game_directories):
            if progress_callback:
                progress_callback(idx / total_dirs * 100, g_dir.name)

            for root_str, dirs, files in os.walk(g_dir):
                root_path = Path(root_str)
                depth = len(root_path.relative_to(g_dir).parts)
                if depth > 3:
                    dirs.clear()
                    continue

                dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d.lower(), pat.lower()) for pat in exclude_dirs)]
                
                for file in files:
                    if file.lower().endswith(".exe"):
                        if any(fnmatch.fnmatch(file.lower(), pat.lower()) for pat in exclude_files):
                            continue
                        
                        file_path = root_path / file
                        try:
                            if file_path.stat().st_size < 50 * 1024:
                                continue
                        except Exception:
                            continue

                        parent_name = file_path.parent.name
                        if parent_name.lower() in ["bin", "win32", "win64", "x64", "x86"]:
                            game_name = file_path.parent.parent.name
                        else:
                            game_name = parent_name

                        games_found.append({
                            'game_name': game_name,
                            'exe_name': file,
                            'path': str(file_path),
                            'folder': str(file_path.parent)
                        })

        if progress_callback:
            progress_callback(100.0, "Scan completed successfully!")

        self.log(f"Incremental Steam scan completed. Found {len(games_found)} targets.")
        return games_found

    def add_custom_game_path(self, target_path):
        p = Path(target_path)
        if not p.exists():
            return None

        games_found = []
        if p.is_file() and p.suffix.lower() == ".exe":
            parent_name = p.parent.name
            game_name = p.parent.parent.name if parent_name.lower() in ["bin", "win32", "win64", "x64", "x86"] else parent_name
            games_found.append({
                'game_name': game_name,
                'exe_name': p.name,
                'path': str(p),
                'folder': str(p.parent)
            })
        elif p.is_dir():
            exclude_dirs = ["*dependencies*", "*repro*", "*shadercache*", "*_CommonRedist*", "*vcredist*", "*DirectX*"]
            exclude_files = ["*unins*", "*setup*", "*crash*", "*update*", "*redist*"]
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d.lower(), pat.lower()) for pat in exclude_dirs)]
                for file in files:
                    if file.lower().endswith(".exe"):
                        if any(fnmatch.fnmatch(file.lower(), pat.lower()) for pat in exclude_files):
                            continue
                        file_path = Path(root) / file
                        if file_path.stat().st_size > 50 * 1024:
                            parent_name = file_path.parent.name
                            game_name = file_path.parent.parent.name if parent_name.lower() in ["bin", "win32", "win64", "x64", "x86"] else parent_name
                            games_found.append({
                                'game_name': game_name,
                                'exe_name': file,
                                'path': str(file_path),
                                'folder': str(file_path.parent)
                            })
        return games_found

    def download_dxvk(self, legacy=False, progress_callback=None):
        self._ensure_temp_dir()
        
        ver_prefix = "dxvk-legacy-1.10.3" if legacy else "dxvk-latest"
        legacy_unpacked_path = self.temp_dir / "dxvk-1.10.3"
        latest_unpacked_path = None
        
        latest_dirs = list(self.temp_dir.glob("dxvk-[2-9]*"))
        if latest_dirs and latest_dirs[0].is_dir():
            latest_unpacked_path = latest_dirs[0]

        if legacy and legacy_unpacked_path.exists():
            self.log(f"Using pre-cached Legacy DXVK 1.10.3 package in: {legacy_unpacked_path}")
            return legacy_unpacked_path
        elif not legacy and latest_unpacked_path and latest_unpacked_path.exists():
            self.log(f"Using pre-cached Latest DXVK package in: {latest_unpacked_path}")
            return latest_unpacked_path

        self.log(f"Downloading required package: {'Legacy v1.10.3' if legacy else 'Latest release'}")

        if legacy:
            download_url = "https://github.com/doitsujin/dxvk/releases/download/v1.10.3/dxvk-1.10.3.tar.gz"
            tar_name = "dxvk-1.10.3.tar.gz"
        else:
            try:
                url = "https://api.github.com/repos/doitsujin/dxvk/releases/latest"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode())
                
                assets = data.get('assets', [])
                tar_asset = [a for a in assets if a.get('name', '').endswith('.tar.gz')][0]
                download_url = tar_asset['browser_download_url']
                tar_name = tar_asset['name']
            except Exception as e:
                self.log(f"GitHub API query failed: {e}. Falling back to mirror direct link.")
                download_url = "https://github.com/doitsujin/dxvk/releases/download/v2.4/dxvk-2.4.tar.gz"
                tar_name = "dxvk-2.4.tar.gz"

        tar_path = self.temp_dir / tar_name
        try:
            req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req) as response:
                total_size = int(response.info().get('Content-Length', 0))
                bytes_read = 0
                block_size = 128 * 1024
                
                with open(tar_path, 'wb') as f:
                    while True:
                        block = response.read(block_size)
                        if not block:
                            break
                        f.write(block)
                        bytes_read += len(block)
                        if progress_callback and total_size > 0:
                            percent = (bytes_read / total_size) * 100
                            progress_callback(percent)
            
            self.log("Download complete. Extracting tarball...")
            if progress_callback:
                progress_callback(-1)

            with tarfile.open(tar_path, "r:gz") as tar:
                tar.extractall(path=self.temp_dir)
            
            tar_path.unlink(missing_ok=True)
            
            if legacy:
                if legacy_unpacked_path.exists():
                    return legacy_unpacked_path
            else:
                unpacked_dirs = [d for d in self.temp_dir.glob("dxvk-[2-9]*") if d.is_dir()]
                if unpacked_dirs:
                    return unpacked_dirs[0]
                    
        except Exception as e:
            self.log(f"Critical error downloading/extracting DXVK: {e}")
        return None

    def remove_or_rename_file(self, filepath):
        p = Path(filepath)
        if not p.exists():
            return True
        try:
            p.unlink()
            return True
        except Exception:
            try:
                trash_path = p.parent / f"{p.name}.TRASH_{os.getpid()}"
                p.rename(trash_path)
                try:
                    trash_path.unlink()
                except Exception:
                    pass
                return True
            except Exception as e:
                self.log(f"Could not purge locked file {p.name}: {e}")
                return False

    def install_vulkanizer(self, game_info, dxvk_base_dir, preset="Best", vsync=1, buffering=3, hud="fps", enable_logs=False, spoof_vram=False, api_override="Auto"):
        if not dxvk_base_dir or not dxvk_base_dir.exists():
            self.log("Selected DXVK package folder is missing!")
            return False

        game_folder = Path(game_info['folder'])
        game_path = Path(game_info['path'])
        exe_name = game_info['exe_name']
        arch = game_info['arch']
        
        # Переопределение API, если пользователь выбрал это в интерфейсе
        if api_override != "Auto":
            api = api_override
            self.log(f"API Override applied: Forcing {api} DLL deployment.")
        else:
            api = game_info.get('api', 'Unknown')

        self.log(f"Deploying custom DLL files from: {dxvk_base_dir}")

        proc_name = exe_name.lower().replace(".exe", "")
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.run(["taskkill", "/F", "/IM", f"{proc_name}.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo=startupinfo)
        except Exception:
            pass

        all_dlls = ["d3d11.dll", "dxgi.dll", "d3d9.dll", "d3d10core.dll"]
        
        # Для DX9 теперь ВСЕГДА ставим и dxgi.dll, чтобы избежать любых проблем с хуками
        if api == "DX9":
            needed_dlls = ["d3d9.dll", "dxgi.dll"]
        elif api == "DX10":
            needed_dlls = ["d3d10core.dll", "dxgi.dll"]
        elif api == "DX11":
            needed_dlls = ["d3d11.dll", "dxgi.dll"]
        else:
            needed_dlls = all_dlls

        for dll in all_dlls:
            target_dll = game_folder / dll
            backup_dll = game_folder / f"{dll}.bak"
            
            if target_dll.exists():
                try:
                    info_raw = target_dll.read_bytes()
                    if b"DXVK" in info_raw or b"doitsujin" in info_raw:
                        self.remove_or_rename_file(target_dll)
                        continue
                except Exception:
                    pass

                if not backup_dll.exists():
                    try:
                        shutil.copy2(target_dll, backup_dll)
                        self.log(f"Original Windows DLL backed up: {dll}")
                    except Exception as e:
                        self.log(f"Backup failed for {dll}: {e}")
                
                self.remove_or_rename_file(target_dll)

        arch_bin_folder = dxvk_base_dir / arch
        if not arch_bin_folder.exists() and arch == "x32":
            arch_bin_folder = dxvk_base_dir / "x86"

        for dll in needed_dlls:
            source_file = arch_bin_folder / dll
            target_file = game_folder / dll
            if source_file.exists():
                try:
                    shutil.copy2(source_file, target_file)
                    try:
                        ctypes.windll.kernel32.DeleteFileW(f"{target_file}:Zone.Identifier")
                    except Exception:
                        pass
                except Exception as e:
                    self.log(f"Failed to deploy DLL {dll}: {e}")

        conf_lines = [
            "# VULKANIZER PRO CONFIG - Optimized by AI & True Gamers",
            "dxvk.enableGraphicsPipelineLibrary = auto",
            "dxvk.enableAsync = True",
            "dxvk.gplAsyncCache = True",
            "dxvk.enableStateCacheCompression = True",
            "dxvk.presentWait = True",
            "dxvk.maxFrameLatency = 1",
            "dxvk.latencySleep = True",
            "d3d11.maxFrameLatency = 1",
            "d3d11.zeroInitWorkgroupMemory = True",
            "dxvk.useRawSsbo = True"
        ]

        if self.gpu_vendor == "NVIDIA":
            conf_lines.append("dxvk.shrinkNvidiaHvvHeap = True")
            
        if spoof_vram:
            self.log("Applying GTA 4 / Old Engine compatibility tweaks & GPU Spoofing (4096 MB / GTX 680)")
            conf_lines.extend([
                "# GTA 4 / OLD ENGINES COMPATIBILITY & SPOOFING FIX",
                "dxvk.customVendorId = 10de",    # NVIDIA Vendor ID
                "dxvk.customDeviceId = 1180",    # NVIDIA GeForce GTX 680 Device ID
                "dxvk.maxVideoMemory = 3072",
                "d3d9.maxAvailableMemory = 4096", # Даем полные 4GB для движка
                "d3d9.deferSurfaceCreation = True"
            ])
            # Генерируем commandline.txt в папке игры
            cmdline_path = game_folder / "commandline.txt"
            try:
                with open(cmdline_path, 'w') as f:
                    f.write("-nomemrestrict\n-norestrictions\n-availablevidmem 4096\n")
                self.log("Generated commandline.txt for legacy uncap.")
            except Exception as e:
                self.log(f"Failed to generate commandline.txt: {e}")

        if enable_logs:
            conf_lines.append("dxvk.logLevel = info")
        else:
            conf_lines.append("dxvk.logLevel = none")

        if hud == "fps":
            conf_lines.append("dxvk.hud = fps")
        elif hud == "extended":
            conf_lines.append("dxvk.hud = fps,frametimes,compiler,gpuload,memory,pipelines")
        elif hud == "full":
            conf_lines.append("dxvk.hud = api,version,devinfo,fps,frametimes,compiler,gpl,pipelines,memory,gpuload")
        else:
            conf_lines.append("# dxvk.hud (Disabled)")

        conf_lines.append(f"dxgi.syncInterval = {vsync}")
        conf_lines.append(f"d3d9.presentInterval = {vsync}")
        conf_lines.append(f"dxgi.numBackBuffers = {buffering}")
        conf_lines.append(f"d3d9.numBackBuffers = {buffering}")

        if preset == "Cinematic":
            conf_lines.extend([
                "# PRESET: CINEMATIC ULTRA",
                "dxvk.samplerAnisotropy = 16",
                "d3d11.samplerAnisotropy = 16",
                "d3d9.samplerAnisotropy = 16",
                "d3d11.mipLODBias = -2.0",
                "d3d11.forceSampleRateShading = True",
                "d3d9.forceSampleRateShading = True",
                "d3d11.maxTessFactor = 16",
                "d3d11.relaxedBarriers = True",
                "d3d11.cachedDynamicResources = true"
            ])
        elif preset == "Ultra":
            conf_lines.extend([
                "# PRESET: ULTRA PERFORMANCE",
                "dxvk.samplerAnisotropy = 16",
                "d3d11.samplerAnisotropy = 16",
                "d3d9.samplerAnisotropy = 16",
                "d3d11.mipLODBias = -1.0",
                "d3d11.forceSampleRateShading = True",
                "d3d11.maxTessFactor = 8"
            ])
        elif preset == "Best":
            conf_lines.extend([
                "# PRESET: BEST PICTURE RESOLUTION",
                "dxvk.samplerAnisotropy = 16",
                "d3d11.samplerAnisotropy = 16",
                "d3d9.samplerAnisotropy = 16",
                "d3d11.mipLODBias = -0.5",
                "d3d11.forceSampleRateShading = True",
                "d3d11.maxTessFactor = 4"
            ])
        elif preset == "Balance":
            conf_lines.extend([
                "# PRESET: BALANCED FRAME DELIVERY",
                "dxvk.samplerAnisotropy = 8",
                "d3d11.samplerAnisotropy = 8",
                "d3d9.samplerAnisotropy = 8",
                "d3d11.mipLODBias = 0.0",
                "d3d11.maxTessFactor = 4"
            ])

        conf_lines.append(f"dxvk.numCompilerThreads = {self.cpu_cores}")

        conf_file = game_folder / "dxvk.conf"
        try:
            with open(conf_file, 'w', encoding='ascii') as f:
                f.write("\n".join(conf_lines))
        except Exception as e:
            self.log(f"Failed to write dxvk.conf: {e}")

        if self.check_admin() and winreg:
            try:
                reg_prio_path = f"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\{exe_name}\\PerfOptions"
                key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, reg_prio_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "CpuPriorityClass", 0, winreg.REG_DWORD, 3)
                winreg.CloseKey(key)
                self.log("Set executable high CPU priority class in Windows registry.")
            except Exception as e:
                self.log(f"Failed to apply Windows registry CPU execution policy: {e}")

        self.log(f"Vulkanizer deployment success: {game_info['game_name']}")
        return True

    def uninstall_vulkanizer(self, game_info):
        game_folder = Path(game_info['folder'])
        exe_name = game_info['exe_name']
        all_dlls = ["d3d11.dll", "dxgi.dll", "d3d9.dll", "d3d10core.dll"]

        proc_name = exe_name.lower().replace(".exe", "")
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.run(["taskkill", "/F", "/IM", f"{proc_name}.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo=startupinfo)
        except Exception:
            pass

        self.log(f"Removing Vulkanizer custom binaries for {game_info['game_name']}...")

        cache_files = list(game_folder.glob("*.dxvk-cache"))
        for cache in cache_files:
            self.remove_or_rename_file(cache)

        for dll in all_dlls:
            target_dll = game_folder / dll
            backup_dll = game_folder / f"{dll}.bak"

            if target_dll.exists():
                try:
                    info_raw = target_dll.read_bytes()
                    if b"DXVK" in info_raw or b"doitsujin" in info_raw:
                        self.remove_or_rename_file(target_dll)
                except Exception:
                    pass

            if backup_dll.exists():
                try:
                    shutil.move(str(backup_dll), str(target_dll))
                    self.log(f"Original game DLL restored: {dll}")
                except Exception:
                    try:
                        shutil.copy2(backup_dll, target_dll)
                        self.remove_or_rename_file(backup_dll)
                    except Exception as e:
                        self.log(f"Restoration failed for {dll}: {e}")

        conf_file = game_folder / "dxvk.conf"
        if conf_file.exists():
            self.remove_or_rename_file(conf_file)

        extra_trash = ["vulkan-1.dll", "opengl32.dll", "d3d12.dll", "ReShade.ini", "ReShade.log", "commandline.txt"]
        for trash in extra_trash:
            t_path = game_folder / trash
            if t_path.exists():
                self.remove_or_rename_file(t_path)

        if self.check_admin() and winreg:
            try:
                reg_prio_path = f"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\{exe_name}"
                winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, f"{reg_prio_path}\\PerfOptions")
                winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, reg_prio_path)
            except Exception:
                pass

        if winreg:
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers", 0, winreg.KEY_ALL_ACCESS)
                winreg.DeleteValue(key, game_info['path'])
                winreg.CloseKey(key)
            except Exception:
                pass

        self.log(f"Uninstall complete for: {game_info['game_name']}")
        return True

    def clean_game_cache(self, game_info):
        game_folder = Path(game_info['folder'])
        self.log(f"Clearing cache states for {game_info['game_name']}...")
        cleaned = False

        cache_files = list(game_folder.glob("*.dxvk-cache"))
        for cache in cache_files:
            if self.remove_or_rename_file(cache):
                cleaned = True

        global_path_str = os.environ.get("DXVK_STATE_CACHE_PATH")
        if global_path_str:
            global_path = Path(global_path_str)
            if global_path.exists():
                cache_file_name = game_info['exe_name'].replace(".exe", ".dxvk-cache")
                g_cache = global_path / cache_file_name
                if g_cache.exists():
                    if self.remove_or_rename_file(g_cache):
                        cleaned = True
        return cleaned

    def reset_game_profile(self, game_info):
        self.log(f"Starting configuration profile reset for {game_info['game_name']}...")
        docs = Path(os.path.expanduser("~/Documents"))
        local_app_data = Path(os.environ.get("LOCALAPPDATA", ""))
        roaming_app_data = Path(os.environ.get("APPDATA", ""))
        
        target_files = ["GamerProfile.xml", "system.xml", "GraphicsConfig.xml", "settings.xml", "display.ini", "config.ini", "user.settings", "pc_settings.bin"]
        clean_name = re.sub(r'[^a-zA-Z0-9]', '*', game_info['game_name'])
        clean_name = re.sub(r'\*+', '*', clean_name).strip('*')
        
        search_dirs = [
            docs / clean_name,
            docs / "My Games" / clean_name,
            local_app_data / clean_name,
            roaming_app_data / clean_name,
            docs / "Ubisoft" / clean_name
        ]

        deleted_count = 0
        for s_dir in search_dirs:
            if s_dir.parent.exists():
                matched_folders = list(s_dir.parent.glob(s_dir.name))
                for folder in matched_folders:
                    if folder.is_dir():
                        for tf in target_files:
                            for found_file in folder.rglob(tf):
                                if self.remove_or_rename_file(found_file):
                                    self.log(f"Purged profile config: {found_file}")
                                    deleted_count += 1
        return deleted_count > 0

    def create_desktop_shortcut(self, game_info):
        desktop = Path(os.path.expanduser("~/Desktop"))
        lnk_path = desktop / f"{game_info['game_name']} Vulkan.lnk"
        self.log(f"Creating desktop shortcut: {lnk_path}")
        try:
            vbs_script = (
                f'Set sh = CreateObject("WScript.Shell")\n'
                f'Set shortcut = sh.CreateShortcut("{str(lnk_path)}")\n'
                f'shortcut.TargetPath = "{game_info["path"]}"\n'
                f'shortcut.WorkingDirectory = "{game_info["folder"]}"\n'
                f'shortcut.Save()'
            )
            vbs_temp = self.temp_dir / "shortcut.vbs"
            vbs_temp.write_text(vbs_script, encoding='utf-8')
            
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.run(["cscript", "/nologo", str(vbs_temp)], startupinfo=startupinfo)
            vbs_temp.unlink(missing_ok=True)
            return True
        except Exception as e:
            self.log(f"Failed to create shortcut: {e}")
            return False

    def check_tweak_status(self, tweak_id):
        if winreg is None:
            return "inactive"

        try:
            if tweak_id == "cache":
                val = os.environ.get("DXVK_STATE_CACHE_PATH")
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ)
                    val, _ = winreg.QueryValueEx(key, "DXVK_STATE_CACHE_PATH")
                    winreg.CloseKey(key)
                except Exception:
                    pass
                return "active" if val == "C:\\DXVK_Cache" else "inactive"

            elif tweak_id == "gamemode":
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar", 0, winreg.KEY_READ)
                val, _ = winreg.QueryValueEx(key, "AutoGameModeEnabled")
                winreg.CloseKey(key)
                return "active" if val == 1 else "inactive"

            elif tweak_id == "gamedvr":
                key1 = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"System\GameConfigStore", 0, winreg.KEY_READ)
                val1, _ = winreg.QueryValueEx(key1, "GameDVR_Enabled")
                winreg.CloseKey(key1)
                
                key2 = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\GameDVR", 0, winreg.KEY_READ)
                val2, _ = winreg.QueryValueEx(key2, "AppCaptureEnabled")
                winreg.CloseKey(key2)
                return "active" if (val1 == 0 and val2 == 0) else "inactive"

            elif tweak_id == "power":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                result = subprocess.run(["powercfg", "/getactivescheme"], capture_output=True, text=True, startupinfo=startupinfo)
                out = result.stdout.lower()
                if "e9a42b02-d5df-448d-aa00-03f14749eb61" in out or "ultimate performance" in out:
                    return "active"
                elif "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c" in out or "high performance" in out:
                    return "active"
                return "inactive"

            elif tweak_id == "priority":
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\PriorityControl", 0, winreg.KEY_READ)
                val, _ = winreg.QueryValueEx(key, "Win32PrioritySeparation")
                winreg.CloseKey(key)
                return "active" if val == 26 else "inactive"

            elif tweak_id == "hags":
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers", 0, winreg.KEY_READ)
                val, _ = winreg.QueryValueEx(key, "HwSchMode")
                winreg.CloseKey(key)
                return "active" if val == 2 else "inactive"

            elif tweak_id == "network":
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", 0, winreg.KEY_READ)
                resp, _ = winreg.QueryValueEx(key, "SystemResponsiveness")
                thro, _ = winreg.QueryValueEx(key, "NetworkThrottlingIndex")
                winreg.CloseKey(key)
                is_disabled = (thro == -1 or thro == 4294967295)
                return "active" if (resp == 0 and is_disabled) else "inactive"

            elif tweak_id == "nagle":
                interfaces_path = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"
                main_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, interfaces_path, 0, winreg.KEY_READ)
                info = winreg.QueryInfoKey(main_key)
                active_count = 0
                match_count = 0
                for i in range(info[0]):
                    subkey_name = winreg.EnumKey(main_key, i)
                    sub_key = winreg.OpenKey(main_key, subkey_name, 0, winreg.KEY_READ)
                    try:
                        has_ip = False
                        try:
                            ip, _ = winreg.QueryValueEx(sub_key, "IPAddress")
                            if isinstance(ip, list):
                                if ip and ip[0] != '0.0.0.0':
                                    has_ip = True
                            elif ip and ip != '0.0.0.0':
                                has_ip = True
                        except Exception:
                            pass
                        
                        if not has_ip:
                            try:
                                dhcp, _ = winreg.QueryValueEx(sub_key, "DhcpIPAddress")
                                if dhcp and dhcp != '0.0.0.0':
                                    has_ip = True
                            except Exception:
                                pass
                        
                        if has_ip:
                            active_count += 1
                            try:
                                val1, _ = winreg.QueryValueEx(sub_key, "TcpAckFrequency")
                                val2, _ = winreg.QueryValueEx(sub_key, "TCPNoDelay")
                                if val1 == 1 and val2 == 1:
                                    match_count += 1
                            except Exception:
                                pass
                    except Exception:
                        pass
                    finally:
                        winreg.CloseKey(sub_key)
                winreg.CloseKey(main_key)
                return "active" if (active_count > 0 and match_count == active_count) or (match_count > 0) else "inactive"

            elif tweak_id == "faststart":
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Power", 0, winreg.KEY_READ)
                val, _ = winreg.QueryValueEx(key, "HiberbootEnabled")
                winreg.CloseKey(key)
                return "active" if val == 0 else "inactive"

            elif tweak_id == "hpet":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                result = subprocess.run(["bcdedit"], capture_output=True, text=True, startupinfo=startupinfo)
                if "disabledynamictick      Yes" in result.stdout:
                    return "active"
                return "inactive"

            elif tweak_id == "aero":
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", 0, winreg.KEY_READ)
                val, _ = winreg.QueryValueEx(key, "EnableTransparency")
                winreg.CloseKey(key)
                return "active" if val == 0 else "inactive"

        except Exception:
            pass
        return "inactive"

    def toggle_tweak(self, tweak_id, current_state):
        if not self.check_admin() or winreg is None:
            self.log("Registry updates require Administrator elevation!")
            return False

        target_state = "active" if current_state == "inactive" else "inactive"
        self.log(f"Toggling OS tweak: {tweak_id} -> {target_state}")

        try:
            if tweak_id == "cache":
                if target_state == "active":
                    cache_dir = Path("C:\\DXVK_Cache")
                    cache_dir.mkdir(exist_ok=True)
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE)
                    winreg.SetValueEx(key, "DXVK_STATE_CACHE_PATH", 0, winreg.REG_SZ, "C:\\DXVK_Cache")
                    winreg.CloseKey(key)
                    os.environ["DXVK_STATE_CACHE_PATH"] = "C:\\DXVK_Cache"
                else:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)
                    try:
                        winreg.DeleteValue(key, "DXVK_STATE_CACHE_PATH")
                    except Exception:
                        pass
                    winreg.CloseKey(key)
                    os.environ.pop("DXVK_STATE_CACHE_PATH", None)

            elif tweak_id == "gamemode":
                val = 1 if target_state == "active" else 0
                key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar", 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "AutoGameModeEnabled", 0, winreg.REG_DWORD, val)
                winreg.CloseKey(key)

            elif tweak_id == "gamedvr":
                val_dvr = 0 if target_state == "active" else 1
                val_cap = 0 if target_state == "active" else 1
                
                key1 = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, r"System\GameConfigStore", 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key1, "GameDVR_Enabled", 0, winreg.REG_DWORD, val_dvr)
                winreg.CloseKey(key1)
                
                key2 = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\GameDVR", 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key2, "AppCaptureEnabled", 0, winreg.REG_DWORD, val_cap)
                winreg.CloseKey(key2)

            elif tweak_id == "power":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                if target_state == "active":
                    result = subprocess.run(["powercfg", "-duplicatescheme", "e9a42b02-d5df-448d-aa00-03f14749eb61"], capture_output=True, text=True, startupinfo=startupinfo)
                    guid = "e9a42b02-d5df-448d-aa00-03f14749eb61"
                    if "e9a42b02" not in result.stdout:
                        subprocess.run(["powercfg", "-duplicatescheme", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"], startupinfo=startupinfo)
                        guid = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
                    
                    subprocess.run(["powercfg", "/setactive", guid], startupinfo=startupinfo)
                    
                    subprocess.run(["powercfg", "/change", "monitor-timeout-ac", "0"], startupinfo=startupinfo)
                    subprocess.run(["powercfg", "/change", "monitor-timeout-dc", "0"], startupinfo=startupinfo)
                    subprocess.run(["powercfg", "/change", "standby-timeout-ac", "0"], startupinfo=startupinfo)
                    subprocess.run(["powercfg", "/change", "standby-timeout-dc", "0"], startupinfo=startupinfo)
                    subprocess.run(["powercfg", "/change", "disk-timeout-ac", "0"], startupinfo=startupinfo)
                    subprocess.run(["powercfg", "/change", "disk-timeout-dc", "0"], startupinfo=startupinfo)
                    subprocess.run(["powercfg", "/change", "hibernate-timeout-ac", "0"], startupinfo=startupinfo)
                    subprocess.run(["powercfg", "/change", "hibernate-timeout-dc", "0"], startupinfo=startupinfo)
                else:
                    subprocess.run(["powercfg", "/setactive", "381b4222-f694-41f0-9685-ff5bb260df2e"], startupinfo=startupinfo)
                    subprocess.run(["powercfg", "/change", "monitor-timeout-ac", "15"], startupinfo=startupinfo)
                    subprocess.run(["powercfg", "/change", "standby-timeout-ac", "30"], startupinfo=startupinfo)
                    subprocess.run(["powercfg", "/change", "disk-timeout-ac", "20"], startupinfo=startupinfo)

            elif tweak_id == "priority":
                val = 26 if target_state == "active" else 2
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\PriorityControl", 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "Win32PrioritySeparation", 0, winreg.REG_DWORD, val)
                winreg.CloseKey(key)

            elif tweak_id == "hags":
                val = 2 if target_state == "active" else 1
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers", 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "HwSchMode", 0, winreg.REG_DWORD, val)
                winreg.CloseKey(key)

            elif tweak_id == "network":
                resp_val = 0 if target_state == "active" else 20
                thro_val = 4294967295 if target_state == "active" else 10
                
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "SystemResponsiveness", 0, winreg.REG_DWORD, resp_val)
                winreg.SetValueEx(key, "NetworkThrottlingIndex", 0, winreg.REG_DWORD, thro_val)
                winreg.CloseKey(key)
                
                task_key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games"
                task_key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, task_key_path, 0, winreg.KEY_SET_VALUE)
                if target_state == "active":
                    winreg.SetValueEx(task_key, "Priority", 0, winreg.REG_DWORD, 6)
                    winreg.SetValueEx(task_key, "Scheduling Category", 0, winreg.REG_SZ, "High")
                    winreg.SetValueEx(task_key, "SFIO Priority", 0, winreg.REG_SZ, "High")
                else:
                    winreg.SetValueEx(task_key, "Priority", 0, winreg.REG_DWORD, 2)
                    winreg.SetValueEx(task_key, "Scheduling Category", 0, winreg.REG_SZ, "Medium")
                    winreg.SetValueEx(task_key, "SFIO Priority", 0, winreg.REG_SZ, "Normal")
                winreg.CloseKey(task_key)

            elif tweak_id == "nagle":
                interfaces_path = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"
                main_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, interfaces_path, 0, winreg.KEY_ALL_ACCESS)
                info = winreg.QueryInfoKey(main_key)
                for i in range(info[0]):
                    subkey_name = winreg.EnumKey(main_key, i)
                    sub_key = winreg.OpenKey(main_key, subkey_name, 0, winreg.KEY_ALL_ACCESS)
                    try:
                        is_nic = False
                        for val_name in ["IPAddress", "DhcpIPAddress"]:
                            try:
                                winreg.QueryValueEx(sub_key, val_name)
                                is_nic = True
                                break
                            except Exception:
                                pass
                        
                        if is_nic:
                            if target_state == "active":
                                winreg.SetValueEx(sub_key, "TcpAckFrequency", 0, winreg.REG_DWORD, 1)
                                winreg.SetValueEx(sub_key, "TCPNoDelay", 0, winreg.REG_DWORD, 1)
                            else:
                                try:
                                    winreg.DeleteValue(sub_key, "TcpAckFrequency")
                                except Exception:
                                    pass
                                try:
                                    winreg.DeleteValue(sub_key, "TCPNoDelay")
                                except Exception:
                                    pass
                    except Exception:
                        pass
                    finally:
                        winreg.CloseKey(sub_key)
                winreg.CloseKey(main_key)

            elif tweak_id == "faststart":
                val = 0 if target_state == "active" else 1
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Power", 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "HiberbootEnabled", 0, winreg.REG_DWORD, val)
                winreg.CloseKey(key)

            elif tweak_id == "hpet":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                if target_state == "active":
                    subprocess.run(["bcdedit", "/set", "useplatformclock", "false"], startupinfo=startupinfo)
                    subprocess.run(["bcdedit", "/set", "disabledynamictick", "yes"], startupinfo=startupinfo)
                else:
                    subprocess.run(["bcdedit", "/deletevalue", "useplatformclock"], startupinfo=startupinfo)
                    subprocess.run(["bcdedit", "/deletevalue", "disabledynamictick"], startupinfo=startupinfo)

            elif tweak_id == "aero":
                val = 0 if target_state == "active" else 1
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "EnableTransparency", 0, winreg.REG_DWORD, val)
                winreg.CloseKey(key)

            self.log(f"Tweak application success: {tweak_id} -> {target_state}")
            return True
        except Exception as e:
            self.log(f"Failed to execute tweak toggle: {e}")
        return False

    def clean_gpu_cache(self):
        self.log("Initiating comprehensive driver-level graphics cache cleaning...")
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        user_profile = os.environ.get("USERPROFILE", "")
        
        cache_paths = [
            Path(local_app_data) / "NVIDIA" / "DXCache",
            Path(local_app_data) / "NVIDIA" / "GLCache",
            Path(user_profile) / "AppData" / "LocalLow" / "NVIDIA" / "PerDriverVersion" / "DXCache",
            Path(local_app_data) / "AMD" / "DxCache"
        ]

        deleted_count = 0
        for path in cache_paths:
            if path.exists():
                self.log(f"Purging shader directory: {path}")
                try:
                    for f in path.rglob("*"):
                        if f.is_file():
                            if self.remove_or_rename_file(f):
                                deleted_count += 1
                except Exception as e:
                    self.log(f"Error listing files in {path}: {e}")
        self.log(f"Graphics shader cleanup complete. Safely removed {deleted_count} stale cache files.")
        return True

    def reset_all_tweaks(self):
        self.log("Resetting all system modifications to factory defaults...")
        tweaks = ["cache", "gamemode", "gamedvr", "power", "priority", "hags", "network", "nagle", "faststart", "hpet", "aero"]
        for t in tweaks:
            self.toggle_tweak(t, "active")
        self.log("All system performance tweaks have been safely reverted.")
        return True

class VulkanizerApp:
    def __init__(self, root):
        self.root = root
        self.model = VulkanizerModel(console_callback=self.write_console)
        self.lang = 'RUS'
        
        self.root.title("ВУЛКАНИЗАТОР ПРО v0.66")
        self.root.geometry("1150x750")
        self.root.minsize(1050, 680)
        self.root.configure(bg=THEME['bg_main'])

        self.selected_game = None
        self.game_list_widgets = []
        self.tweak_widgets = {}
        self.tweak_states = {}

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure(".", background=THEME['bg_main'], foreground=THEME['text_light'], fieldbackground=THEME['bg_card'])
        self.style.configure("TProgressbar", thickness=15, troughcolor=THEME['bg_sidebar'], background=THEME['accent_cyan'])

        sys.stdout = self
        sys.stderr = self

        self.create_layout()
        self.root.state('zoomed')
        self.root.after(100, self.run_startup_checks)

    def run_startup_checks(self):
        if not self.model.check_admin():
            self.show_admin_warning()
        else:
            self.show_disclaimer_overlay()

    def tr(self, key):
        return LOCALIZATION[self.lang].get(key, key)

    def write_console(self, text):
        if hasattr(self, 'console_text') and self.console_text.winfo_exists():
            self.console_text.configure(state='normal')
            self.console_text.insert(tk.END, text)
            self.console_text.see(tk.END)
            self.console_text.configure(state='disabled')

    def write(self, text):
        self.write_console(text)

    def flush(self):
        pass

    def create_layout(self):
        self.sidebar = tk.Frame(self.root, bg=THEME['bg_sidebar'], width=260)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.main_container = tk.Frame(self.root, bg=THEME['bg_main'])
        self.main_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        logo_label = tk.Label(self.sidebar, text="🐱 /\\_/\\", font=("Consolas", 18, "bold"), bg=THEME['bg_sidebar'], fg=THEME['accent_pink'])
        logo_label.pack(pady=(20, 5))
        title_label = tk.Label(self.sidebar, text=self.tr('title'), font=("Segoe UI", 13, "bold"), bg=THEME['bg_sidebar'], fg=THEME['accent_cyan'])
        title_label.pack()
        subtitle_label = tk.Label(self.sidebar, text="alpha v0.66 wrapper pro", font=("Segoe UI", 8, "italic"), bg=THEME['bg_sidebar'], fg=THEME['text_gray'])
        subtitle_label.pack(pady=(0, 15))

        self.nav_buttons = {}
        tabs_def = [
            ('games', "games", self.tr('tab_games')),
            ('tweaks', "tweaks", self.tr('tab_tweaks')),
            ('console', "console", self.tr('tab_console')),
            ('about', "about", self.tr('tab_about'))
        ]

        for tab_id, icon_id, text_val in tabs_def:
            emoji = "🎮  " if tab_id == 'games' else "⚙️  " if tab_id == 'tweaks' else "🛠️  " if tab_id == 'console' else "ℹ️  "
            btn = tk.Button(
                self.sidebar, text=f"{emoji}{text_val}", font=("Segoe UI", 10, "bold"),
                bg=THEME['bg_sidebar'], fg=THEME['text_gray'], activebackground=THEME['bg_card_sel'],
                activeforeground=THEME['text_light'], relief=tk.FLAT, bd=0, anchor='w', padx=20,
                command=lambda tid=tab_id: self.switch_tab(tid)
            )
            btn.pack(fill=tk.X, pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=THEME['bg_card_sel'], fg=THEME['text_light']))
            btn.bind("<Leave>", lambda e, b=btn, tid=tab_id: self.nav_button_leave(b, tid))
            self.nav_buttons[tab_id] = btn

        lang_frame = tk.Frame(self.sidebar, bg=THEME['bg_sidebar'])
        lang_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20, padx=20)
        
        self.btn_lang_rus = tk.Button(lang_frame, text="🇷🇺 RUS", font=("Segoe UI", 8, "bold"), bg=THEME['bg_card'], fg=THEME['accent_cyan'], relief=tk.FLAT, bd=0, command=lambda: self.set_language('RUS'))
        self.btn_lang_rus.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        self.btn_lang_eng = tk.Button(lang_frame, text="🇬🇧 ENG", font=("Segoe UI", 8, "bold"), bg=THEME['bg_sidebar'], fg=THEME['text_gray'], relief=tk.FLAT, bd=0, command=lambda: self.set_language('ENG'))
        self.btn_lang_eng.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=2)

        self.frames = {
            'games': tk.Frame(self.main_container, bg=THEME['bg_main']),
            'tweaks': tk.Frame(self.main_container, bg=THEME['bg_main']),
            'console': tk.Frame(self.main_container, bg=THEME['bg_main']),
            'about': tk.Frame(self.main_container, bg=THEME['bg_main'])
        }

        self.setup_games_tab()
        self.setup_tweaks_tab()
        self.setup_console_tab()
        self.setup_about_tab()

        self.switch_tab('games')

    def nav_button_leave(self, button, tab_id):
        if self.current_tab != tab_id:
            button.configure(bg=THEME['bg_sidebar'], fg=THEME['text_gray'])
        else:
            button.configure(bg=THEME['bg_card'], fg=THEME['accent_cyan'])

    def switch_tab(self, tab_id):
        self.current_tab = tab_id
        for tid, frame in self.frames.items():
            if tid == tab_id:
                frame.pack(fill=tk.BOTH, expand=True)
                self.nav_buttons[tid].configure(bg=THEME['bg_card'], fg=THEME['accent_cyan'])
            else:
                frame.pack_forget()
                self.nav_buttons[tid].configure(bg=THEME['bg_sidebar'], fg=THEME['text_gray'])

    def set_language(self, language_code):
        self.lang = language_code
        self.root.title(self.tr('title'))
        
        if self.lang == 'RUS':
            self.btn_lang_rus.configure(bg=THEME['bg_card'], fg=THEME['accent_cyan'])
            self.btn_lang_eng.configure(bg=THEME['bg_sidebar'], fg=THEME['text_gray'])
        else:
            self.btn_lang_rus.configure(bg=THEME['bg_sidebar'], fg=THEME['text_gray'])
            self.btn_lang_eng.configure(bg=THEME['bg_card'], fg=THEME['accent_cyan'])

        for widget in self.main_container.winfo_children():
            widget.pack_forget()
        self.sidebar.destroy()
        self.create_layout()
        self.update_game_cards()
        if self.selected_game:
            self.select_game(self.selected_game)
        self.update_tweak_statuses()

    def setup_games_tab(self):
        f = self.frames['games']
        
        left_panel = tk.Frame(f, bg=THEME['bg_main'], width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(15, 5), pady=15)
        left_panel.pack_propagate(False)

        actions_ribbon = tk.Frame(left_panel, bg=THEME['bg_main'])
        actions_ribbon.pack(fill=tk.X, pady=(0, 10))

        btn_scan = tk.Button(
            actions_ribbon, text=self.tr('btn_scan_steam'), font=("Segoe UI", 9, "bold"),
            bg=THEME['accent_cyan'], fg=THEME['text_dark'], relief=tk.FLAT, bd=0, padx=8, pady=5,
            command=self.run_steam_scan_thread
        )
        btn_scan.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        btn_folder = tk.Button(
            actions_ribbon, text="📁", font=("Segoe UI", 9, "bold"),
            bg=THEME['bg_card'], fg=THEME['text_light'], relief=tk.FLAT, bd=0, padx=12, pady=5,
            command=self.add_custom_folder
        )
        btn_folder.pack(side=tk.LEFT, padx=2)
        ToolTip(btn_folder, lambda: self.tr('tooltip_folder'))

        btn_file = tk.Button(
            actions_ribbon, text="⚙️", font=("Segoe UI", 9, "bold"),
            bg=THEME['bg_card'], fg=THEME['text_light'], relief=tk.FLAT, bd=0, padx=12, pady=5,
            command=self.add_custom_file
        )
        btn_file.pack(side=tk.LEFT, padx=2)
        ToolTip(btn_file, lambda: self.tr('tooltip_file'))

        self.scan_frame = tk.Frame(left_panel, bg=THEME['bg_main'])
        self.scan_status_lbl = tk.Label(self.scan_frame, text="", font=("Segoe UI", 8, "italic"), bg=THEME['bg_main'], fg=THEME['accent_cyan'], anchor="w")
        self.scan_status_lbl.pack(fill=tk.X, pady=(0, 2))
        self.scan_progress_bar = ttk.Progressbar(self.scan_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.scan_progress_bar.pack(fill=tk.X, pady=(0, 8))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.filter_game_cards())
        self.search_entry = tk.Entry(
            left_panel, textvariable=self.search_var, bg=THEME['bg_card'], fg=THEME['text_light'],
            insertbackground=THEME['accent_cyan'], font=("Segoe UI", 9, "bold"), relief=tk.FLAT, bd=0,
            highlightthickness=1, highlightbackground=THEME['bg_sidebar'], highlightcolor=THEME['accent_cyan']
        )
        self.search_entry.pack(fill=tk.X, pady=(0, 10), ipady=6, padx=2)
        self.set_search_placeholder()

        self.cards_scroll_canvas = tk.Canvas(left_panel, bg=THEME['bg_main'], bd=0, highlightthickness=0)
        self.cards_scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=self.cards_scroll_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cards_scroll_canvas.configure(yscrollcommand=scrollbar.set)

        self.cards_frame = tk.Frame(self.cards_scroll_canvas, bg=THEME['bg_main'])
        self.cards_frame.bind("<Configure>", lambda e: self.cards_scroll_canvas.configure(scrollregion=self.cards_scroll_canvas.bbox("all")))
        self.cards_scroll_canvas.create_window((0, 0), window=self.cards_frame, anchor="nw", width=380)

        self.right_panel = tk.Frame(f, bg=THEME['bg_card'], bd=1, highlightbackground=THEME['bg_sidebar'], highlightthickness=1)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 15), pady=15)
        self.show_no_game_selected_placeholder()

        self.update_game_cards()

    def set_search_placeholder(self):
        self.search_entry.insert(0, self.tr('search_placeholder'))
        self.search_entry.configure(fg=THEME['text_gray'])
        self.search_entry.bind("<FocusIn>", self.clear_search_placeholder)
        self.search_entry.bind("<FocusOut>", self.restore_search_placeholder)

    def clear_search_placeholder(self, event):
        if self.search_entry.get() == self.tr('search_placeholder'):
            self.search_entry.delete(0, tk.END)
            self.search_entry.configure(fg=THEME['text_light'])

    def restore_search_placeholder(self, event):
        if not self.search_entry.get().strip():
            self.search_entry.insert(0, self.tr('search_placeholder'))
            self.search_entry.configure(fg=THEME['text_gray'])

    def filter_game_cards(self):
        query = self.search_var.get().lower()
        placeholder = self.tr('search_placeholder').lower()
        if query == placeholder or not query.strip():
            for widget in self.cards_frame.winfo_children():
                widget.pack(fill=tk.X, pady=4, padx=2)
            return

        for idx, game in enumerate(self.model.games):
            widget = self.game_list_widgets[idx]
            match_name = game['game_name'].lower()
            match_exe = game['exe_name'].lower()
            if query in match_name or query in match_exe:
                widget.pack(fill=tk.X, pady=4, padx=2)
            else:
                widget.pack_forget()

    def update_game_cards(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        self.game_list_widgets.clear()

        if not self.model.games:
            lbl = tk.Label(self.cards_frame, text=self.tr('no_games'), wraplength=350, font=("Segoe UI", 10), bg=THEME['bg_main'], fg=THEME['text_gray'])
            lbl.pack(pady=40, padx=20)
            return

        for idx, game in enumerate(self.model.games):
            card = tk.Frame(self.cards_frame, bg=THEME['bg_card'], bd=1, relief=tk.FLAT, pady=10, padx=12)
            card.pack(fill=tk.X, pady=4, padx=2)
            
            accent = THEME['accent_cyan'] if self.selected_game == game else THEME['bg_sidebar']
            card.configure(highlightbackground=accent, highlightthickness=1)

            lbl_name = tk.Label(card, text=game['game_name'], font=("Segoe UI", 11, "bold"), anchor="w", bg=THEME['bg_card'], fg=THEME['text_light'])
            lbl_name.pack(fill=tk.X)

            lbl_sub = tk.Label(card, text=game['exe_name'], font=("Consolas", 8), anchor="w", bg=THEME['bg_card'], fg=THEME['text_gray'])
            lbl_sub.pack(fill=tk.X)

            badge_strip = tk.Frame(card, bg=THEME['bg_card'])
            badge_strip.pack(fill=tk.X, pady=(5, 0))

            api_color = THEME['accent_green'] if game.get('api') in ["DX11", "DX9"] else THEME['accent_pink']
            badge_api = tk.Label(badge_strip, text=f" {game.get('api', 'Unknown')} ", font=("Segoe UI", 8, "bold"), bg=THEME['bg_sidebar'], fg=api_color)
            badge_api.pack(side=tk.LEFT, padx=(0, 5))

            badge_arch = tk.Label(badge_strip, text=f" {game.get('arch', 'x64')} ", font=("Segoe UI", 8, "bold"), bg=THEME['bg_sidebar'], fg=THEME['accent_cyan'])
            badge_arch.pack(side=tk.LEFT)

            is_vulkanized = (Path(game['folder']) / "dxvk.conf").exists()
            if is_vulkanized:
                tag = tk.Label(badge_strip, text=" VULKANIZED ", font=("Segoe UI", 8, "bold"), bg=THEME['accent_green'], fg=THEME['text_dark'])
                tag.pack(side=tk.RIGHT)

            for widget in [card, lbl_name, lbl_sub, badge_strip, badge_api, badge_arch]:
                widget.bind("<Button-1>", lambda e, g=game: self.select_game(g))

            self.game_list_widgets.append(card)

    def select_game(self, game_info):
        self.selected_game = game_info
        self.update_game_cards()
        self.show_game_control_panel(game_info)

    def show_no_game_selected_placeholder(self):
        for widget in self.right_panel.winfo_children():
            widget.destroy()

        placeholder = tk.Frame(self.right_panel, bg=THEME['bg_card'])
        placeholder.pack(fill=tk.BOTH, expand=True)

        lbl_cat = tk.Label(placeholder, text="🐾\nSelect a Game to Configure", font=("Segoe UI", 12, "bold"), bg=THEME['bg_card'], fg=THEME['text_gray'])
        lbl_cat.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def show_game_control_panel(self, game):
        for widget in self.right_panel.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.right_panel, bg=THEME['bg_card'], bd=0, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.right_panel, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        panel = tk.Frame(canvas, bg=THEME['bg_card'], padx=15, pady=15)
        panel.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=panel, anchor="nw", width=420)

        title_lbl = tk.Label(panel, text=self.tr('game_settings_for').format(game['game_name']), font=("Segoe UI", 13, "bold"), bg=THEME['bg_card'], fg=THEME['accent_cyan'], anchor="w")
        title_lbl.pack(fill=tk.X, pady=(0, 15))

        tk.Label(panel, text=self.tr('dxvk_version_title'), font=("Segoe UI", 10, "bold"), bg=THEME['bg_card'], fg=THEME['text_light'], anchor="w").pack(fill=tk.X, pady=(0, 5))
        self.dxvk_version_var = tk.BooleanVar(value=False)
        
        legacy_frame = tk.Frame(panel, bg=THEME['bg_sidebar'], pady=5, padx=8)
        legacy_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Radiobutton(
            legacy_frame, text=self.tr('dxvk_latest'), variable=self.dxvk_version_var, value=False,
            font=("Segoe UI", 9), bg=THEME['bg_sidebar'], fg=THEME['text_light'],
            selectcolor=THEME['bg_card'], relief=tk.FLAT, bd=0
        ).pack(anchor="w", pady=2)
        
        tk.Radiobutton(
            legacy_frame, text=self.tr('dxvk_legacy'), variable=self.dxvk_version_var, value=True,
            font=("Segoe UI", 9), bg=THEME['bg_sidebar'], fg=THEME['text_light'],
            selectcolor=THEME['bg_card'], relief=tk.FLAT, bd=0
        ).pack(anchor="w", pady=2)

        # Блок принудительного выбора (Оверрайд) API
        tk.Label(panel, text=self.tr('api_override_title'), font=("Segoe UI", 10, "bold"), bg=THEME['bg_card'], fg=THEME['text_light'], anchor="w").pack(fill=tk.X, pady=(0, 5))
        self.api_override_var = tk.StringVar(value="Auto")
        
        override_frame = tk.Frame(panel, bg=THEME['bg_sidebar'], pady=5, padx=8)
        override_frame.pack(fill=tk.X, pady=(0, 15))
        
        for val in ["Auto", "DX11", "DX10", "DX9", "All"]:
            tk.Radiobutton(
                override_frame, text=val, variable=self.api_override_var, value=val,
                font=("Segoe UI", 9), bg=THEME['bg_sidebar'], fg=THEME['text_light'],
                selectcolor=THEME['bg_card'], relief=tk.FLAT, bd=0
            ).pack(side=tk.LEFT, padx=3)

        tk.Label(panel, text=self.tr('select_preset'), font=("Segoe UI", 10, "bold"), bg=THEME['bg_card'], fg=THEME['text_light'], anchor="w").pack(fill=tk.X, pady=(0, 5))
        
        self.preset_var = tk.StringVar(value="Best")
        presets = [
            ("Cinematic", self.tr('preset_cinematic'), self.tr('preset_cinematic_desc')),
            ("Ultra", self.tr('preset_ultra'), self.tr('preset_ultra_desc')),
            ("Best", self.tr('preset_best'), self.tr('preset_best_desc')),
            ("Balance", self.tr('preset_balance'), self.tr('preset_balance_desc')),
            ("Vanilla", self.tr('preset_vanilla'), self.tr('preset_vanilla_desc'))
        ]

        preset_frame = tk.Frame(panel, bg=THEME['bg_card'])
        preset_frame.pack(fill=tk.X, pady=(0, 15))

        for preset_id, name, desc in presets:
            btn_frame = tk.Frame(preset_frame, bg=THEME['bg_card'])
            btn_frame.pack(fill=tk.X, pady=2)
            
            rbtn = tk.Radiobutton(
                btn_frame, text=name, variable=self.preset_var, value=preset_id,
                font=("Segoe UI", 10, "bold"), bg=THEME['bg_card'], fg=THEME['text_light'],
                activebackground=THEME['bg_card'], activeforeground=THEME['accent_cyan'],
                selectcolor=THEME['bg_sidebar'], relief=tk.FLAT, bd=0
            )
            rbtn.pack(side=tk.LEFT, anchor="w")

            desc_lbl = tk.Label(btn_frame, text=desc, font=("Segoe UI", 8), bg=THEME['bg_card'], fg=THEME['text_gray'], wraplength=280, justify=tk.LEFT, anchor="w")
            desc_lbl.pack(fill=tk.X, padx=(25, 0))

            tooltip_text = f"⚙️ {name}\n\n📝 {desc}"
            ToolTip(rbtn, lambda t=tooltip_text: t)
            ToolTip(desc_lbl, lambda t=tooltip_text: t)
            ToolTip(btn_frame, lambda t=tooltip_text: t)

        tk.Label(panel, text=self.tr('vsync_buffering'), font=("Segoe UI", 10, "bold"), bg=THEME['bg_card'], fg=THEME['text_light'], anchor="w").pack(fill=tk.X, pady=(0, 5))
        
        self.vsync_var = tk.IntVar(value=1)
        vsync_opt = [
            (1, self.tr('vsync_on')),
            (0, self.tr('vsync_off')),
            (2, self.tr('vsync_half'))
        ]
        vsync_frame = tk.Frame(panel, bg=THEME['bg_sidebar'], pady=5, padx=8)
        vsync_frame.pack(fill=tk.X, pady=(0, 10))
        for val, opt_name in vsync_opt:
            tk.Radiobutton(
                vsync_frame, text=opt_name, variable=self.vsync_var, value=val,
                font=("Segoe UI", 9), bg=THEME['bg_sidebar'], fg=THEME['text_light'],
                selectcolor=THEME['bg_card'], relief=tk.FLAT, bd=0
            ).pack(side=tk.LEFT, padx=5)

        self.buffering_var = tk.IntVar(value=3)
        buffering_opt = [
            (2, "2x (Double)"),
            (3, "3x (Triple)"),
            (4, "4x (Quad)")
        ]
        buffering_frame = tk.Frame(panel, bg=THEME['bg_sidebar'], pady=5, padx=8)
        buffering_frame.pack(fill=tk.X, pady=(0, 15))
        for val, opt_name in buffering_opt:
            tk.Radiobutton(
                buffering_frame, text=opt_name, variable=self.buffering_var, value=val,
                font=("Segoe UI", 9), bg=THEME['bg_sidebar'], fg=THEME['text_light'],
                selectcolor=THEME['bg_card'], relief=tk.FLAT, bd=0
            ).pack(side=tk.LEFT, padx=5)

        tk.Label(panel, text=self.tr('overlay_mgmt'), font=("Segoe UI", 10, "bold"), bg=THEME['bg_card'], fg=THEME['text_light'], anchor="w").pack(fill=tk.X, pady=(0, 5))
        
        self.hud_var = tk.StringVar(value="fps")
        hud_opt = [
            ("none", self.tr('overlay_none')),
            ("fps", self.tr('overlay_fps')),
            ("extended", self.tr('overlay_extended')),
            ("full", self.tr('overlay_full'))
        ]
        hud_frame = tk.Frame(panel, bg=THEME['bg_card'])
        hud_frame.pack(fill=tk.X, pady=(0, 15))
        for val, opt_name in hud_opt:
            tk.Radiobutton(
                hud_frame, text=opt_name, variable=self.hud_var, value=val,
                font=("Segoe UI", 9), bg=THEME['bg_card'], fg=THEME['text_light'],
                selectcolor=THEME['bg_sidebar'], relief=tk.FLAT, bd=0
            ).pack(anchor="w", pady=1)

        self.logs_var = tk.BooleanVar(value=False)
        chk_logs = tk.Checkbutton(
            panel, text=self.tr('log_enabled'), variable=self.logs_var,
            font=("Segoe UI", 9), bg=THEME['bg_card'], fg=THEME['text_light'],
            selectcolor=THEME['bg_sidebar'], relief=tk.FLAT, bd=0, activebackground=THEME['bg_card']
        )
        chk_logs.pack(anchor="w", pady=(0, 15))

        # Спуфинг видеокарты
        spoof_frame = tk.Frame(panel, bg=THEME['bg_sidebar'], bd=0)
        spoof_frame.pack(fill=tk.X, pady=(0, 15))

        spoof_lbl = tk.Label(
            spoof_frame, text=self.tr('spoof_vram'), font=("Segoe UI", 9, "bold"),
            bg=THEME['bg_sidebar'], fg=THEME['accent_pink'], wraplength=280, justify=tk.LEFT, anchor="w"
        )
        spoof_lbl.pack(side=tk.LEFT, padx=(10, 5), pady=10, fill=tk.X, expand=True)

        self.spoof_vram_var = tk.BooleanVar(value=False)
        self.btn_spoof = tk.Button(
            spoof_frame, text=self.tr('btn_off'), font=("Segoe UI", 9, "bold"),
            bg=THEME['bg_card'], fg=THEME['text_gray'], relief=tk.FLAT, bd=0, width=6,
            command=self.toggle_spoof_vram
        )
        self.btn_spoof.pack(side=tk.RIGHT, padx=10, pady=10)

        btn_install = tk.Button(
            panel, text=self.tr('install_vulkanizer'), font=("Segoe UI", 11, "bold"),
            bg=THEME['accent_pink'], fg=THEME['text_light'], relief=tk.FLAT, bd=0, pady=10,
            command=self.run_install_thread
        )
        btn_install.pack(fill=tk.X, pady=(0, 20))

        tk.Label(panel, text=self.tr('maintenance_tools'), font=("Segoe UI", 10, "bold"), bg=THEME['bg_card'], fg=THEME['accent_pink'], anchor="w").pack(fill=tk.X, pady=(0, 8))
        
        btn_grid = tk.Frame(panel, bg=THEME['bg_card'])
        btn_grid.pack(fill=tk.X)

        m_tools = [
            (self.tr('btn_clean_cache'), self.clean_cache),
            (self.tr('btn_reset_settings'), self.reset_profile),
            (self.tr('btn_deep_uninstall'), self.uninstall_game),
            (self.tr('btn_desktop_shortcut'), self.create_shortcut),
            (self.tr('btn_launch_game'), self.launch_game)
        ]

        for text, cmd in m_tools:
            btn = tk.Button(btn_grid, text=text, font=("Segoe UI", 9, "bold"), bg=THEME['bg_sidebar'], fg=THEME['text_light'], relief=tk.FLAT, bd=0, pady=6, anchor="w", padx=10, command=cmd)
            btn.pack(fill=tk.X, pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=THEME['bg_card_sel']))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=THEME['bg_sidebar']))

        self.status_lbl = tk.Label(panel, text=self.tr('status_ready'), font=("Segoe UI", 9, "italic"), bg=THEME['bg_card'], fg=THEME['text_gray'], anchor="w")
        self.status_lbl.pack(fill=tk.X, pady=(20, 0))

        self.progress_bar = ttk.Progressbar(panel, orient=tk.HORIZONTAL, mode='determinate')

    def setup_tweaks_tab(self):
        f = self.frames['tweaks']
        
        header = tk.Frame(f, bg=THEME['bg_main'], pady=15, padx=20)
        header.pack(fill=tk.X)

        tk.Label(header, text="⚙️ " + self.tr('tab_tweaks'), font=("Segoe UI", 16, "bold"), bg=THEME['bg_main'], fg=THEME['accent_cyan']).pack(anchor="w")
        tk.Label(header, text=self.tr('global_tweaks_desc'), font=("Segoe UI", 9), bg=THEME['bg_main'], fg=THEME['text_gray']).pack(anchor="w", pady=(5, 0))

        btn_reset_all = tk.Button(
            header, text=self.tr('btn_reset_all_tweaks'), font=("Segoe UI", 9, "bold"),
            bg=THEME['accent_pink'], fg=THEME['text_light'], relief=tk.FLAT, bd=0, padx=12, pady=6,
            command=self.reset_all_system_tweaks
        )
        btn_reset_all.pack(anchor="w", pady=(10, 0))

        canvas = tk.Canvas(f, bg=THEME['bg_main'], bd=0, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        scrollbar = ttk.Scrollbar(f, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 20))
        canvas.configure(yscrollcommand=scrollbar.set)

        self.tweaks_list_frame = tk.Frame(canvas, bg=THEME['bg_main'])
        canvas.create_window((0, 0), window=self.tweaks_list_frame, anchor="nw")
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas.find_withtag("all")[0], width=event.width)
            self.root.after(10, self.reflow_tweak_labels)

        canvas.bind("<Configure>", on_canvas_configure)
        self.tweaks_canvas = canvas

        self.render_tweak_cards()

    def reflow_tweak_labels(self):
        w = self.tweaks_canvas.winfo_width() - 40
        if w < 400:
            w = 400
        for tweak_id, widgets in self.tweak_widgets.items():
            if 'lbl_title' in widgets and widgets['lbl_title'].winfo_exists():
                widgets['lbl_title'].configure(wraplength=w - 220)
            if 'lbl_desc' in widgets and widgets['lbl_desc'].winfo_exists():
                widgets['lbl_desc'].configure(wraplength=w - 220)

    def render_tweak_cards(self):
        for widget in self.tweaks_list_frame.winfo_children():
            widget.destroy()
        self.tweak_widgets.clear()

        tweaks_definitions = [
            ("cache", self.tr('tweak_cache_title'), self.tr('tweak_cache_desc')),
            ("gamemode", self.tr('tweak_gamemode_title'), self.tr('tweak_gamemode_desc')),
            ("gamedvr", self.tr('tweak_gamedvr_title'), self.tr('tweak_gamedvr_desc')),
            ("gpucache", self.tr('tweak_gpucache_title'), self.tr('tweak_gpucache_desc')),
            ("power", self.tr('tweak_power_title'), self.tr('tweak_power_desc')),
            ("priority", self.tr('tweak_prio_title'), self.tr('tweak_prio_desc')),
            ("hags", self.tr('tweak_hags_title'), self.tr('tweak_hags_desc')),
            ("network", self.tr('tweak_network_title'), self.tr('tweak_network_desc')),
            ("nagle", self.tr('tweak_nagle_title'), self.tr('tweak_nagle_desc')),
            ("faststart", self.tr('tweak_faststart_title'), self.tr('tweak_faststart_desc')),
            ("hpet", self.tr('tweak_hpet_title'), self.tr('tweak_hpet_desc')),
            ("tempclean", self.tr('tweak_tempclean_title'), self.tr('tweak_tempclean_desc')),
            ("aero", self.tr('tweak_aero_title'), self.tr('tweak_aero_desc'))
        ]

        for tweak_id, title, desc in tweaks_definitions:
            card = tk.Frame(self.tweaks_list_frame, bg=THEME['bg_card'], bd=1, relief=tk.FLAT, padx=15, pady=12)
            card.pack(fill=tk.X, pady=5, expand=True)

            text_sub_frame = tk.Frame(card, bg=THEME['bg_card'])
            text_sub_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

            lbl_title = tk.Label(text_sub_frame, text=title, font=("Segoe UI", 11, "bold"), bg=THEME['bg_card'], fg=THEME['text_light'], anchor="w", justify=tk.LEFT)
            lbl_title.pack(fill=tk.X)

            lbl_desc = tk.Label(text_sub_frame, text=desc, font=("Segoe UI", 9), bg=THEME['bg_card'], fg=THEME['text_gray'], justify=tk.LEFT, anchor="w")
            lbl_desc.pack(fill=tk.X, pady=(3, 0))

            control_sub_frame = tk.Frame(card, bg=THEME['bg_card'])
            control_sub_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

            status_indicator = tk.Label(control_sub_frame, text="QUERYING", font=("Segoe UI", 8, "bold"), bg=THEME['bg_sidebar'], fg=THEME['accent_cyan'], width=18)
            status_indicator.pack(side=tk.LEFT, padx=(0, 10))

            btn_toggle = tk.Button(
                control_sub_frame, text="...", font=("Segoe UI", 9, "bold"),
                bg=THEME['bg_sidebar'], fg=THEME['text_light'], relief=tk.FLAT, bd=0, padx=14, pady=6,
                command=lambda tid=tweak_id: self.toggle_system_tweak_thread(tid)
            )
            btn_toggle.pack(side=tk.RIGHT)
            
            btn_toggle.bind("<Enter>", lambda e, b=btn_toggle: b.configure(bg=THEME['bg_card_sel']))
            btn_toggle.bind("<Leave>", lambda e, b=btn_toggle, tid=tweak_id: self.update_tweak_button_leave_style(b, tid))

            self.tweak_widgets[tweak_id] = {
                'status': status_indicator,
                'toggle_btn': btn_toggle,
                'lbl_title': lbl_title,
                'lbl_desc': lbl_desc
            }

        self.update_tweak_statuses()

    def update_tweak_button_leave_style(self, button, tweak_id):
        if tweak_id in ["gpucache", "tempclean"]:
            button.configure(bg=THEME['bg_sidebar'], fg=THEME['accent_cyan'])
            return
            
        status = self.tweak_states.get(tweak_id, "inactive")
        if status == "active":
            button.configure(bg="#3a111a", fg=THEME['accent_pink'])
        else:
            button.configure(bg="#113a20", fg=THEME['accent_green'])

    def update_tweak_statuses(self):
        def run_check():
            def get_dir_size(path):
                total = 0
                try:
                    for entry in os.scandir(path):
                        if entry.is_file():
                            total += entry.stat().st_size
                        elif entry.is_dir():
                            total += get_dir_size(entry.path)
                except Exception:
                    pass
                return total

            results = {}
            for tweak_id in self.tweak_widgets.keys():
                if tweak_id in ["gpucache", "tempclean"]:
                    results[tweak_id] = ("inactive", 0)
                    continue
                
                status = self.model.check_tweak_status(tweak_id)
                cache_size = 0
                if tweak_id == "cache" and status == "active":
                    cache_size = get_dir_size("C:\\DXVK_Cache")
                results[tweak_id] = (status, cache_size)
            
            self.root.after(0, lambda: self._apply_tweak_statuses(results))
        
        threading.Thread(target=run_check, daemon=True).start()

    def _apply_tweak_statuses(self, results):
        for tweak_id, (status, cache_size) in results.items():
            self.tweak_states[tweak_id] = status
            if tweak_id not in self.tweak_widgets:
                continue
            widgets = self.tweak_widgets[tweak_id]
            
            if tweak_id in ["gpucache", "tempclean"]:
                widgets['status'].configure(text=self.tr('status_cleaner'), fg=THEME['text_gray'])
                widgets['toggle_btn'].configure(text=self.tr('tweak_btn_clear'), bg=THEME['bg_sidebar'], fg=THEME['accent_cyan'])
                continue
                
            if status == "active":
                if tweak_id == "cache":
                    if cache_size > 1024 * 1024:
                        size_str = f" ({cache_size / (1024 * 1024):.1f} MB)"
                    elif cache_size > 1024:
                        size_str = f" ({cache_size / 1024:.0f} KB)"
                    else:
                        size_str = " (0 KB)"
                    active_text = self.tr('status_active') + size_str
                else:
                    active_text = self.tr('status_active')

                widgets['status'].configure(text=active_text, fg=THEME['accent_green'])
                widgets['toggle_btn'].configure(text=self.tr('tweak_btn_disable'), bg="#3a111a", fg=THEME['accent_pink'])
            else:
                widgets['status'].configure(text=self.tr('status_inactive'), fg=THEME['accent_pink'])
                widgets['toggle_btn'].configure(text=self.tr('tweak_btn_enable'), bg="#113a20", fg=THEME['accent_green'])

    def setup_console_tab(self):
        f = self.frames['console']
        header = tk.Frame(f, bg=THEME['bg_main'], pady=15, padx=20)
        header.pack(fill=tk.X)
        tk.Label(header, text="🛠️ " + self.tr('tab_console'), font=("Segoe UI", 16, "bold"), bg=THEME['bg_main'], fg=THEME['accent_cyan']).pack(anchor="w")

        self.console_text = tk.Text(f, bg=THEME['bg_sidebar'], fg=THEME['accent_cyan'], insertbackground=THEME['text_light'], font=("Consolas", 9), relief=tk.FLAT, bd=0, padx=10, pady=10)
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.console_text.configure(state='disabled')

    def setup_about_tab(self):
        f = self.frames['about']
        header = tk.Frame(f, bg=THEME['bg_main'], pady=15, padx=20)
        header.pack(fill=tk.X)
        tk.Label(header, text="ℹ️ " + self.tr('tab_about'), font=("Segoe UI", 16, "bold"), bg=THEME['bg_main'], fg=THEME['accent_cyan']).pack(anchor="w")

        about_scroll_frame = tk.Frame(f, bg=THEME['bg_main'])
        about_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        self.about_text_widget = tk.Text(about_scroll_frame, bg=THEME['bg_card'], fg=THEME['text_light'], font=("Segoe UI", 10), wrap=tk.WORD, relief=tk.FLAT, bd=0, padx=15, pady=15)
        self.about_text_widget.pack(fill=tk.BOTH, expand=True)
        self.update_about_text_links()

    def update_about_text_links(self):
        tb = self.about_text_widget
        tb.configure(state='normal')
        tb.delete("1.0", tk.END)
        tb.insert(tk.END, self.tr('about_text'))
        
        idx = "1.0"
        while True:
            idx = tb.search("@EvilCat_97", idx, nocase=True, stopindex=tk.END)
            if not idx: break
            lastidx = f"{idx}+{len('@EvilCat_97')}c"
            tb.tag_add("tg_link", idx, lastidx)
            idx = lastidx
            
        idx = "1.0"
        while True:
            idx = tb.search("https://github.com/doitsujin/dxvk", idx, nocase=True, stopindex=tk.END)
            if not idx: break
            lastidx = f"{idx}+{len('https://github.com/doitsujin/dxvk')}c"
            tb.tag_add("gh_link", idx, lastidx)
            idx = lastidx

        tb.tag_config("tg_link", foreground=THEME['accent_cyan'], underline=True)
        tb.tag_bind("tg_link", "<Button-1>", lambda e: webbrowser.open("https://t.me/EvilCat_97"))
        tb.tag_bind("tg_link", "<Enter>", lambda e: tb.config(cursor="hand2"))
        tb.tag_bind("tg_link", "<Leave>", lambda e: tb.config(cursor=""))

        tb.tag_config("gh_link", foreground=THEME['accent_cyan'], underline=True)
        tb.tag_bind("gh_link", "<Button-1>", lambda e: webbrowser.open("https://github.com/doitsujin/dxvk"))
        tb.tag_bind("gh_link", "<Enter>", lambda e: tb.config(cursor="hand2"))
        tb.tag_bind("gh_link", "<Leave>", lambda e: tb.config(cursor=""))
        
        tb.configure(state='disabled')

    def show_admin_warning(self):
        warn_win = tk.Toplevel(self.root)
        warn_win.title(self.tr('admin_required'))
        warn_win.geometry("560x300")
        warn_win.resizable(False, False)
        warn_win.configure(bg=THEME['bg_card'])
        warn_win.transient(self.root)
        warn_win.grab_set()

        warn_win.update_idletasks()
        width = warn_win.winfo_width()
        height = warn_win.winfo_height()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
        warn_win.geometry(f"+{x}+{y}")

        admin_lang_frame = tk.Frame(warn_win, bg=THEME['bg_card'])
        admin_lang_frame.pack(anchor="ne", padx=10, pady=5)
        
        btn_rus = tk.Button(admin_lang_frame, text="RU", font=("Segoe UI", 8, "bold"), bg=THEME['bg_sidebar'], fg=THEME['accent_cyan'], relief=tk.FLAT, bd=0, padx=5, command=lambda: [self.set_language_direct('RUS', warn_win), self.update_admin_window(warn_win)])
        btn_rus.pack(side=tk.LEFT, padx=2)
        btn_eng = tk.Button(admin_lang_frame, text="EN", font=("Segoe UI", 8, "bold"), bg=THEME['bg_sidebar'], fg=THEME['text_gray'], relief=tk.FLAT, bd=0, padx=5, command=lambda: [self.set_language_direct('ENG', warn_win), self.update_admin_window(warn_win)])
        btn_eng.pack(side=tk.LEFT, padx=2)

        if self.lang == 'RUS':
            btn_rus.configure(fg=THEME['accent_cyan'])
            btn_eng.configure(fg=THEME['text_gray'])
        else:
            btn_rus.configure(fg=THEME['text_gray'])
            btn_eng.configure(fg=THEME['accent_cyan'])

        self.admin_title_lbl = tk.Label(warn_win, text="🛡️ " + self.tr('admin_required'), font=("Segoe UI", 14, "bold"), bg=THEME['bg_card'], fg=THEME['accent_pink'])
        self.admin_title_lbl.pack(side=tk.TOP, pady=(10, 10))
        
        self.btn_admin_elevate = tk.Button(
            warn_win, text=self.tr('btn_elevate'), font=("Segoe UI", 11, "bold"),
            bg=THEME['accent_cyan'], fg=THEME['text_dark'], relief=tk.FLAT, bd=0, padx=15, pady=8,
            command=self.self_elevate
        )
        self.btn_admin_elevate.pack(side=tk.BOTTOM, pady=(10, 20))

        self.admin_desc_lbl = tk.Label(warn_win, text=self.tr('admin_desc'), font=("Segoe UI", 11), bg=THEME['bg_card'], fg=THEME['text_light'], wraplength=480, justify=tk.CENTER)
        self.admin_desc_lbl.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        warn_win.bind("<Destroy>", lambda e: self.show_disclaimer_overlay())

    def update_admin_window(self, win):
        self.admin_title_lbl.configure(text="🛡️ " + self.tr('admin_required'))
        self.admin_desc_lbl.configure(text=self.tr('admin_desc'))
        self.btn_admin_elevate.configure(text=self.tr('btn_elevate'))
        win.title(self.tr('admin_required'))

    def set_language_direct(self, code, window):
        self.lang = code
        self.root.title(self.tr('title'))

    def self_elevate(self):
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit(0)
        except Exception as e:
            self.model.log(f"Elevation bypass failed: {e}")

    def show_disclaimer_overlay(self):
        if hasattr(self, 'disclaimer_open') and self.disclaimer_open:
            return
        self.disclaimer_open = True

        overlay = tk.Toplevel(self.root)
        overlay.title(self.tr('disclaimer_title'))
        overlay.geometry("820x660")
        overlay.configure(bg=THEME['bg_card'])
        overlay.transient(self.root)
        overlay.grab_set()
        overlay.resizable(False, False)

        overlay.update_idletasks()
        width = overlay.winfo_width()
        height = overlay.winfo_height()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
        overlay.geometry(f"+{x}+{y}")

        lang_control_frame = tk.Frame(overlay, bg=THEME['bg_card'])
        lang_control_frame.pack(anchor="ne", padx=15, pady=10)
        
        btn_rus = tk.Button(lang_control_frame, text="🇷🇺 RUS", font=("Segoe UI", 8, "bold"), bg=THEME['bg_sidebar'], fg=THEME['accent_cyan'], relief=tk.FLAT, bd=0, padx=8, pady=3)
        btn_rus.pack(side=tk.LEFT, padx=3)
        
        btn_eng = tk.Button(lang_control_frame, text="🇬🇧 ENG", font=("Segoe UI", 8, "bold"), bg=THEME['bg_sidebar'], fg=THEME['text_gray'], relief=tk.FLAT, bd=0, padx=8, pady=3)
        btn_eng.pack(side=tk.RIGHT, padx=3)

        if self.lang == 'RUS':
            btn_rus.configure(fg=THEME['accent_cyan'])
            btn_eng.configure(fg=THEME['text_gray'])
        else:
            btn_rus.configure(fg=THEME['text_gray'])
            btn_eng.configure(fg=THEME['accent_cyan'])

        text_box = tk.Text(overlay, bg=THEME['bg_sidebar'], fg=THEME['text_light'], font=("Segoe UI", 11), wrap=tk.WORD, padx=15, pady=15, relief=tk.FLAT, bd=0)

        btn_accept = tk.Button(
            overlay, text=self.tr('accept_risks'), font=("Segoe UI", 12, "bold"),
            bg=THEME['accent_cyan'], fg=THEME['text_dark'], relief=tk.FLAT, bd=0, padx=20, pady=10,
            command=lambda: [overlay.destroy(), setattr(self, 'disclaimer_open', False), self.set_language(self.lang)]
        )

        btn_rus.configure(command=lambda: [self.set_language_direct('RUS', overlay), self.update_disclaimer_view(overlay, text_box, btn_accept, btn_rus, btn_eng)])
        btn_eng.configure(command=lambda: [self.set_language_direct('ENG', overlay), self.update_disclaimer_view(overlay, text_box, btn_accept, btn_rus, btn_eng)])

        self.disc_title_lbl = tk.Label(overlay, text=self.tr('disclaimer_title'), font=("Segoe UI", 18, "bold"), bg=THEME['bg_card'], fg=THEME['accent_pink'])
        self.disc_title_lbl.pack(pady=(5, 10))

        btn_accept.pack(side=tk.BOTTOM, pady=(10, 20))
        text_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        text_box.insert(tk.END, self.tr('disclaimer_text'))
        text_box.configure(state='disabled')

    def update_disclaimer_view(self, overlay, text_box, accept_btn, btn_rus, btn_eng):
        overlay.title(self.tr('disclaimer_title'))
        self.disc_title_lbl.configure(text=self.tr('disclaimer_title'))
        
        text_box.configure(state='normal')
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, self.tr('disclaimer_text'))
        text_box.configure(state='disabled')
        
        accept_btn.configure(text=self.tr('accept_risks'))

        if self.lang == 'RUS':
            btn_rus.configure(fg=THEME['accent_cyan'])
            btn_eng.configure(fg=THEME['text_gray'])
        else:
            btn_rus.configure(fg=THEME['text_gray'])
            btn_eng.configure(fg=THEME['accent_cyan'])

    def run_steam_scan_thread(self):
        self.nav_buttons['games'].configure(state='disabled')
        self.write_console("Starting incremental Steam library scan...\n")
        
        self.scan_frame.pack(fill=tk.X, pady=(0, 10), before=self.search_entry)
        self.scan_progress_bar.configure(value=0)
        self.scan_status_lbl.configure(text="Initializing Steam scanner...")

        def run():
            scanned = self.model.scan_steam_games_iterative(progress_callback=self._update_scan_progress)
            
            for game in scanned:
                game['arch'] = self.model.get_exe_architecture(game['path'])
                game['api'] = self.model.scan_exe_api(game['path'])
            
            self.root.after(0, lambda: self._scan_complete(scanned))

        threading.Thread(target=run, daemon=True).start()

    def _update_scan_progress(self, percent, current_dir_name):
        self.root.after(0, lambda: [
            self.scan_progress_bar.configure(value=percent),
            self.scan_status_lbl.configure(text=f"Scanning: {current_dir_name} ({percent:.1f}%)")
        ])

    def _scan_complete(self, games_list):
        self.model.games = games_list
        self.nav_buttons['games'].configure(state='normal')
        self.scan_frame.pack_forget()
        self.update_game_cards()
        self.write_console(f"Scan complete. Found {len(games_list)} games.\n")

    def add_custom_folder(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            scanned = self.model.add_custom_game_path(dir_path)
            if scanned:
                self.model.games.clear() # Изоляция поиска для ручных папок
                for game in scanned:
                    game['arch'] = self.model.get_exe_architecture(game['path'])
                    game['api'] = self.model.scan_exe_api(game['path'])
                    if not any(g['path'] == game['path'] for g in self.model.games):
                        self.model.games.append(game)
                self.update_game_cards()

    def add_custom_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])
        if file_path:
            scanned = self.model.add_custom_game_path(file_path)
            if scanned:
                self.model.games.clear() # Изоляция поиска для ручных файлов
                for game in scanned:
                    game['arch'] = self.model.get_exe_architecture(game['path'])
                    game['api'] = self.model.scan_exe_api(game['path'])
                    if not any(g['path'] == game['path'] for g in self.model.games):
                        self.model.games.append(game)
                self.update_game_cards()

    def run_install_thread(self):
        if not self.selected_game:
            return

        self.status_lbl.configure(text=self.tr('status_downloading').format(0), fg=THEME['accent_cyan'])
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        self.progress_bar.configure(value=0)

        legacy_choice = self.dxvk_version_var.get()

        def run():
            dxvk_dir = self.model.download_dxvk(legacy=legacy_choice, progress_callback=self._update_progress_from_thread)
            if dxvk_dir:
                self.root.after(0, lambda: self.status_lbl.configure(text=self.tr('status_extracting')))
                
                preset = self.preset_var.get()
                vsync = self.vsync_var.get()
                buffering = self.buffering_var.get()
                hud = self.hud_var.get()
                logs = self.logs_var.get()
                spoof_vram = self.spoof_vram_var.get()
                api_override = self.api_override_var.get()

                install_success = self.model.install_vulkanizer(
                    self.selected_game, dxvk_dir, preset=preset, vsync=vsync,
                    buffering=buffering, hud=hud, enable_logs=logs, spoof_vram=spoof_vram, api_override=api_override
                )
                self.root.after(0, lambda: self._install_finished(install_success))
            else:
                self.root.after(0, lambda: self._install_finished(False))

        threading.Thread(target=run, daemon=True).start()

    def _update_progress_from_thread(self, percent):
        if percent == -1:
            self.root.after(0, lambda: self.progress_bar.configure(mode='indeterminate'))
            self.root.after(0, self.progress_bar.start)
        else:
            self.root.after(0, lambda: self.progress_bar.configure(mode='determinate', value=percent))
            self.root.after(0, lambda: self.status_lbl.configure(text=self.tr('status_downloading').format(percent)))

    def _install_finished(self, success):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        if success:
            self.status_lbl.configure(text=self.tr('status_install_success').format(self.selected_game['game_name']), fg=THEME['accent_green'])
            self.update_game_cards()
            
            # Уникальный помощник для GTA 4
            proc_name = self.selected_game['exe_name'].lower()
            if "gta" in proc_name and self.spoof_vram_var.get():
                launch_args = "-nomemrestrict -norestrictions -availablevidmem 4096"
                try:
                    self.root.clipboard_clear()
                    self.root.clipboard_append(launch_args)
                    self.root.update()
                    messagebox.showwarning(
                        "🚨 КРИТИЧЕСКИ ВАЖНО ДЛЯ GTA 4", 
                        "Современный лаунчер Steam/Rockstar часто полностью ИГНОРИРУЕТ фиксы памяти из папки!\n\n"
                        "Мы скопировали нужные параметры разблокировки в ваш БУФЕР ОБМЕНА.\n\n"
                        "ЧТО НУЖНО СДЕЛАТЬ ПРЯМО СЕЙЧАС:\n"
                        "1. Откройте библиотеку Steam\n"
                        "2. Кликните правой кнопкой мыши по GTA 4 -> Свойства\n"
                        "3. В поле 'Параметры запуска' нажмите Ctrl+V (Вставить)\n\n"
                        f"Должен вставиться этот текст:\n{launch_args}\n\n"
                        "Если у вас пиратка — запускайте игру строго через GTAIV.exe, а не через Launcher."
                    )
                except Exception as e:
                    self.model.log(f"Clipboard action failed: {e}")
        else:
            self.status_lbl.configure(text="❌ Deployment failed! Check the console tab for detailed error logs.", fg=THEME['accent_pink'])

    def toggle_spoof_vram(self):
        self.spoof_vram_var.set(not self.spoof_vram_var.get())
        if self.spoof_vram_var.get():
            self.btn_spoof.configure(text=self.tr('btn_on'), bg=THEME['accent_pink'], fg=THEME['text_dark'])
        else:
            self.btn_spoof.configure(text=self.tr('btn_off'), bg=THEME['bg_card'], fg=THEME['text_gray'])

    def clean_cache(self):
        if not self.selected_game:
            return
        if self.model.clean_game_cache(self.selected_game):
            self.status_lbl.configure(text=self.tr('status_cache_clean_success'), fg=THEME['accent_green'])
        else:
            self.status_lbl.configure(text="ℹ️ No active dxvk caches found for this target game.", fg=THEME['text_gray'])

    def reset_profile(self):
        if not self.selected_game:
            return
        if self.model.reset_game_profile(self.selected_game):
            self.status_lbl.configure(text=self.tr('status_profile_reset_success'), fg=THEME['accent_green'])
        else:
            self.status_lbl.configure(text="ℹ️ Standard configuration profile files not found in Documents/AppData folders.", fg=THEME['text_gray'])

    def uninstall_game(self):
        if not self.selected_game:
            return
        if self.model.uninstall_vulkanizer(self.selected_game):
            self.status_lbl.configure(text=self.tr('status_uninstall_success').format(self.selected_game['game_name']), fg=THEME['accent_pink'])
            self.update_game_cards()
        else:
            self.status_lbl.configure(text="❌ Failed to uninstall wrapper files cleanly.", fg=THEME['accent_pink'])

    def create_shortcut(self):
        if not self.selected_game:
            return
        if self.model.create_desktop_shortcut(self.selected_game):
            self.status_lbl.configure(text="✅ Shortcut generated successfully on your Desktop!", fg=THEME['accent_green'])
        else:
            self.status_lbl.configure(text="❌ Failed to write the shortcut to your Desktop.", fg=THEME['accent_pink'])

    def launch_game(self):
        if not self.selected_game:
            return
        try:
            self.model.log(f"Launching external process executable: {self.selected_game['path']}")
            subprocess.Popen([self.selected_game['path']], cwd=self.selected_game['folder'])
            self.status_lbl.configure(text="🚀 Game execution instance launched!", fg=THEME['accent_green'])
        except Exception as e:
            self.model.log(f"Launch failed: {e}")
            self.status_lbl.configure(text="❌ Execution instance failed to initialize.", fg=THEME['accent_pink'])

    def toggle_system_tweak_thread(self, tweak_id):
        widget_set = self.tweak_widgets[tweak_id]
        widget_set['toggle_btn'].configure(state='disabled')
        
        current_state = self.tweak_states.get(tweak_id, "inactive")
        
        if tweak_id == "gpucache":
            def run_clean():
                self.model.clean_gpu_cache()
                self.root.after(0, lambda: [
                    widget_set['toggle_btn'].configure(state='normal'),
                    messagebox.showinfo(self.tr('title'), "🧹 GPU drivers cache folders are successfully cleared!")
                ])
            threading.Thread(target=run_clean, daemon=True).start()
            return

        if tweak_id == "tempclean":
            def run_tempclean():
                self.model.log("Cleaning Windows Temp and Prefetch directories...")
                temp_paths = [
                    Path(tempfile.gettempdir()),
                    Path("C:\\Windows\\Temp"),
                    Path("C:\\Windows\\Prefetch")
                ]
                deleted_count = 0
                for path in temp_paths:
                    if path.exists():
                        try:
                            for item in path.glob("*"):
                                try:
                                    if item.is_file():
                                        if self.model.remove_or_rename_file(item):
                                            deleted_count += 1
                                    elif item.is_dir():
                                        shutil.rmtree(item, ignore_errors=True)
                                except:
                                    pass
                        except:
                            pass
                self.model.log(f"System Temp directories cleared. Purged {deleted_count} garbage files.")
                self.root.after(0, lambda: [
                    widget_set['toggle_btn'].configure(state='normal'),
                    messagebox.showinfo(self.tr('title'), f"🧹 Windows Temp/Prefetch folders successfully cleared! Removed {deleted_count} files.")
                ])
            threading.Thread(target=run_tempclean, daemon=True).start()
            return

        def run():
            success = self.model.toggle_tweak(tweak_id, current_state)
            self.root.after(0, lambda: [
                self.update_tweak_statuses(),
                widget_set['toggle_btn'].configure(state='normal')
            ])

        threading.Thread(target=run, daemon=True).start()

    def reset_all_system_tweaks(self):
        def run():
            self.model.reset_all_tweaks()
            self.root.after(0, lambda: [
                self.update_tweak_statuses(),
                messagebox.showinfo(self.tr('title'), "🚨 All system performance parameters reverted to factory Windows standards.")
            ])

        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = VulkanizerApp(root)
    root.mainloop()