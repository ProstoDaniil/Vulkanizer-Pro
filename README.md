======================================================================
                     ВУЛКАНИЗАТОР ПРО (alpha v0.67)
======================================================================

 ЧТО НОВОГО В ВЕРСИИ 0.67 (ЧЕЙНДЖЛОГ):

1. Строгий контроль API (Оверрайд):
   - Полностью удален ненадежный режим "Auto" при установке библиотек.
   - Теперь программа сканирует игру и предлагает подходящий DirectX (как подсказку), но пользователь сам принимает финальное решение.
   - Скрипт установит ТОЛЬКО те DLL, которые вы выбрали вручную (DX9, DX10, DX11 или All). Никакого "захламления" папок лишними библиотеками.

2. Умное добавление папок:
   - Полностью переработана кнопка "Добавить папку".
   - Теперь она не добавляет слепо все .exe файлы из директории (игнорируя лаунчеры, деинсталляторы и т.д.).
   - При выборе папки появляется удобное всплывающее окно со списком найденных игр/файлов. Вы можете галочками отметить только те .exe, которые действительно хотите оптимизировать.

3. Исправление одиночного добавления:
   - Починен баг, из-за которого ломалось ручное добавление одиночного .exe файла (кнопка с шестеренкой).
   - Теперь при добавлении одиночного файла он моментально и корректно выбирается в списке активных игр.

----------------------------------------------------------------------
🇬🇧 ENGLISH VERSION
----------------------------------------------------------------------

======================================================================
                     VULKANIZER PRO (alpha v0.67)
======================================================================

 WHAT'S NEW IN VERSION 0.67 (CHANGELOG):

1. Strict API Control (Override):
   - The unreliable "Auto" mode for library installation has been completely removed.
   - The program now scans the game and suggests the appropriate DirectX version (as a hint), but the user makes the final decision.
   - The script will install ONLY the DLLs you manually select (DX9, DX10, DX11, or All). No more cluttering game folders with unnecessary libraries.

2. Smart Folder Addition:
   - The "Add Folder" button has been completely reworked.
   - It no longer blindly adds all .exe files from a directory (ignoring launchers, uninstallers, etc.).
   - When you select a folder, a convenient pop-up window appears with a list of found games/files. You can use checkboxes to select only the .exe files you actually want to optimize.

3. Single File Addition Fix:
   - Fixed a bug that broke the manual addition of a single .exe file (the gear button).
   - Now, when adding a single file, it is instantly and correctly selected in the active games list.



                     ВУЛКАНИЗАТОР ПРО (alpha v0.66)
  Интеллектуальный оптимизатор & GUI-враппер для перевода игр на Vulkan API
               ДЛЯ ИСТИННЫХ ГЕЙМЕРОВ. ОТ ТЕХ, КТО В ИГРЕ!
======================================================================

ОГЛАВЛЕНИЕ
1. О проекте и благодарности
2. Важные предупреждения и риски
3. Специальные инструкции (Ubisoft, GTA 4)
4. Настройки и Пресеты графики
5. Инструменты обслуживания игр
6. Глобальные системные твики ОС (13 штук)
7. Инструкция по использованию
8. Контакты и Авторы

----------------------------------------------------------------------
1. О ПРОЕКТЕ И БЛАГОДАРНОСТИ
----------------------------------------------------------------------
ВУЛКАНИЗАТОР ПРО — это продвинутая графическая оболочка (враппер) и комплексный оптимизатор операционной системы. 

ВАЖНО: Этот проект НЕ является заменой или альтернативой оригинальному DXVK. Мы глубоко уважаем и ценим титанический труд Филиппа Ребо (doitsujin) и всей команды оригинального DXVK за революцию в трансляции вызовов DirectX 9/10/11 в Vulkan API! Официальный репозиторий DXVK: https://github.com/doitsujin/dxvk.

Наша утилита автоматизирует процесс внедрения:
- Самостоятельно скачивает оригинальные библиотеки с GitHub.
- Анализирует .exe файлы игр, определяя их разрядность (x32/x64) и используемый API (DX9, DX10, DX11).
- Распределяет файлы, разблокирует их в Windows и генерирует оптимальный конфигурационный файл dxvk.conf на основе выбранных вами пресетов.

----------------------------------------------------------------------
2. ВАЖНЫЕ ПРЕДУПРЕЖДЕНИЯ И РИСКИ
----------------------------------------------------------------------
Вулканизатор работает с играми на DirectX 9, 10 и 11. Однако не на всех конфигурациях все игры будут работать! Это зависит от аппаратного обеспечения (видеокарта должна поддерживать Vulkan) и особенностей самого игрового движка.

Что делать, если игра не запускается? (БЕЗ ПАНИКИ)
Скрипт работает максимально безопасно. Перед заменой файлов он делает бэкапы (.bak). Если после установки Вулканизатора игра выдает ошибку, крашится или показывает черный экран, вам не нужно переустанавливать игру.

Просто перейдите в папку с .exe файлом игры и удалите следующие файлы:
- d3d9.dll, d3d10core.dll, d3d11.dll, dxgi.dll
- dxvk.conf

Или воспользуйтесь кнопкой "Удалить Вулканизатор" в самой программе. Игра вернется к своему родному, чистому состоянию на DirectX. Ничего не сломается.

Совет по стабильности: Для максимальной стабильности с Vulkan запускайте игры в режиме "Окно без рамки" (Borderless Windowed). Это предотвращает вылеты при сворачивании (Alt+Tab), убирает задержки ввода и гарантирует стабильную работу оверлеев.

----------------------------------------------------------------------
3. СПЕЦИАЛЬНЫЕ ИНСТРУКЦИИ
----------------------------------------------------------------------
[Игры UBISOFT (Assassin's Creed, Watch Dogs, Far Cry и др.)]
Оверлей Ubisoft Connect часто вызывает моментальные краши при работе с Vulkan API. Если вы устанавливаете Вулканизатор на игры Ubisoft, обязательно выполните эти шаги:
1. Откройте лаунчер Ubisoft Connect.
2. Перейдите в Меню -> Настройки -> вкладка "Интерфейс".
3. Снимите галочку с пункта "Включить внутриигровой оверлей для поддерживаемых игр".
4. Запускайте игру СТРОГО через сам лаунчер Ubisoft Connect, а не напрямую через EXE!

[Ультимативный Фикс GTA 4 (и старые движки)]
Старые движки не умеют работать с современными объемами памяти. В программе есть специальный тумблер "Эмуляция топ-видеокарты GTX 680 (Разблок памяти)".
При его включении:
- Видеокарта маскируется под NVIDIA GTX 680.
- Выделяется жесткий лимит в 4096 МБ видеопамяти.
- Создается файл commandline.txt в папке игры.
- ВНИМАНИЕ: Современные лаунчеры Steam/Rockstar игнорируют файлы в папке. Программа скопирует нужные параметры в ваш буфер обмена (-nomemrestrict -norestrictions -availablevidmem 4096). Обязательно вставьте их в "Параметры запуска" игры в Steam! Если у вас пиратка — запускайте строго через GTAIV.exe.

----------------------------------------------------------------------
4. НАСТРОЙКИ И ПРЕСЕТЫ ГРАФИКИ
----------------------------------------------------------------------
[Выбор версии DXVK]
- Новейшая версия (Latest): v2.4+ (Требует поддержку Vulkan 1.3). Идеально для современных видеокарт.
- Legacy-совместимая: v1.10.3 (Требует поддержку Vulkan 1.1). Специально для старых видеокарт.

[Принудительный выбор API (Оверрайд)]
По умолчанию программа сама определяет API игры. Но иногда игры используют смешанные библиотеки. Вы можете принудительно заставить программу установить библиотеки только для DX9, DX10, DX11 или установить сразу Все.

[Пресеты оптимизации (Генерация dxvk.conf)]
1. Синематик Ультра (Cinematic): Максимальная плавность, 4 буфера, анизотропия 16x, экстремальная детализация LOD (-2.0), принудительный Sample Rate Shading.
2. Ультра качество (Ultra): Баланс высокого качества, анизотропия 16x, детализация LOD (-1.0), тесселяция х8.
3. Лучшая картинка (Best): Четкость и плавность, приоритет FPS, анизотропия 16x, средний LOD (-0.5). Оптимальный выбор.
4. Сбалансированный (Balance): Оптимальное соотношение визуала и FPS, анизотропия 8x, стандартный LOD (0.0).
5. Чистый Vulkan (Vanilla): Только чистая трансляция вызовов DXVK. Никаких графических улучшений, максимальный упор на снижение инпут-лага и высокий приоритет CPU.

[Синхронизация и Буферизация]
ОБЯЗАТЕЛЬНО: В наших пресетах вертикальная синхронизация ВКЛЮЧЕНА ПО УМОЛЧАНИЮ через DXVK. Выключите V-Sync в настройках самой игры, чтобы избежать двойного инпут-лага!
- V-Sync: ВКЛ (Рекомендуется), ВЫКЛ (Мин. задержка, возможны разрывы экрана), ПОЛОВИННЫЙ x2 (для лока 30/60 fps).
- Буферизация: Двойная (2 кадра), Тройная (3 кадра — стандарт), Квадро (4 кадра — для ультра-плавности на мощных ПК).

[Оверлей и Мониторинг (HUD DXVK)]
- Без оверлея: Полностью отключен.
- Минимальный: Только счетчик FPS.
- Расширенный: FPS, фреймтайм, загрузка GPU, компиляция шейдеров, память.
- Полная диагностика: Выводит на экран абсолютно все графики, версии API и статус конвейеров.

----------------------------------------------------------------------
5. ИНСТРУМЕНТЫ ОБСЛУЖИВАНИЯ ИГР
----------------------------------------------------------------------
- Очистить кэш игры: Удаляет файлы *.dxvk-cache. Полезно, если игра начала фризить после обновления драйверов.
- Сбросить настройки игры: Ищет и удаляет файлы конфигурации (GamerProfile.xml, settings.xml и др.) в папках Documents и AppData.
- Удалить Вулканизатор: Глубокая очистка. Удаляет все .dll файлы DXVK, dxvk.conf, возвращает бэкапы оригинальных файлов Windows.
- Создать ярлык: Создает прямой .lnk ярлык на рабочем столе для запуска настроенной игры.

----------------------------------------------------------------------
6. ГЛОБАЛЬНЫЕ СИСТЕМНЫЕ ТВИКИ ОС
----------------------------------------------------------------------
Вулканизатор ПРО включает 13 глубоких оптимизаций операционной системы. Требуется запуск от имени Администратора. Все твики можно откатить одной кнопкой "СБРОСИТЬ ВСЕ ТВИКИ".

1. Единый глобальный кэш DXVK: Переносит кэш всех игр в папку C:\DXVK_Cache.
2. Игровой режим Windows (Game Mode): Принудительно активирует подавление фоновых задач.
3. Отключение Xbox GameDVR: Отключает фоновую циклическую запись экрана.
4. Очистка кэша драйвера GPU: Проводит чистку папок NVIDIA/DXCache, AMD/DxCache.
5. Схема питания "Ultimate Performance": Активирует скрытую схему макс. производительности, запрещает парковку ядер.
6. Приоритеты планировщика CPU: Меняет Win32PrioritySeparation на 26, отдавая макс. ресурсы игре.
7. Аппаратное планирование GPU (HAGS): Управление видеопамятью в обход драйвера ОС.
8. Сетевой стек (MMCSS): Снимает лимит сети, отдает играм приоритет 100%.
9. Алгоритм Нагла (Низкий пинг): Отключает буферизацию пакетов (TcpAckFrequency), снижая задержки.
10. Чистое завершение работы: Отключает быстрый запуск/гибернацию для сброса утечек памяти.
11. Отключение HPET и таймеров: Убирает микро-фризы при резких движениях мыши.
12. Очистка временных файлов: Жестко очищает директории Temp и Prefetch.
13. Отключение прозрачности Windows: Отключает эффекты Aero/Fluent для экономии ресурсов GPU.

----------------------------------------------------------------------
7. ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ
----------------------------------------------------------------------
1. Запустите приложение от имени Администратора.
2. На вкладке "Игры и Настройки" нажмите "Сканировать Steam" или добавьте игру вручную.
3. В появившемся списке выберите игру.
4. Настройте параметры: версию DXVK, пресет графики и оверлей.
5. Нажмите "УСТАНОВИТЬ ВУЛКАНИЗАТОР" и дождитесь загрузки/распаковки библиотек.
6. Нажмите "Запустить игру" (рекомендуется режим "Окно без рамки").

----------------------------------------------------------------------
8. КОНТАКТЫ И АВТОРЫ
----------------------------------------------------------------------
Создатели враппера: EvilCat & AI (Золотой Стандарт)
Модификация и улучшение: Звёздочка
Связь с создателем (Telegram): @EvilCat_97
Проект оригинального транслятора DXVK: https://github.com/doitsujin/dxvk

Помните: вероятность встретить медведя с дробовиком крайне мала, но никогда не равна нулю! Приятной игры без лагов!

//////////////////////////////////////////////////////////////////////////////////////////
======================================================================
                     VULKANIZER PRO (alpha v0.66)
  Intelligent optimizer & GUI-wrapper for translating games to Vulkan API
                   FOR TRUE GAMERS. BY THOSE WHO PLAY!
======================================================================

TABLE OF CONTENTS
1. About the project and credits
2. Important warnings and risks
3. Special instructions (Ubisoft, GTA 4)
4. Settings and Graphics Presets
5. Game maintenance tools
6. Global OS system tweaks (13 tweaks)
7. How to use
8. Contacts and Authors

----------------------------------------------------------------------
1. ABOUT THE PROJECT AND CREDITS
----------------------------------------------------------------------
VULKANIZER PRO is an advanced graphical shell (wrapper) and comprehensive operating system optimizer.

IMPORTANT: This project is NOT a replacement or alternative to the original DXVK. We deeply respect and appreciate the titanic work of Philip Rebo (doitsujin) and the entire original DXVK team for revolutionizing the translation of DirectX 9/10/11 calls into Vulkan API! Official DXVK repository: https://github.com/doitsujin/dxvk.

Our utility automates the deployment process:
- Automatically downloads the original libraries from GitHub.
- Analyzes game .exe files, determining their architecture (x32/x64) and API used (DX9, DX10, DX11).
- Distributes files, unblocks them in Windows, and generates an optimal dxvk.conf configuration file based on your selected presets.

----------------------------------------------------------------------
2. IMPORTANT WARNINGS AND RISKS
----------------------------------------------------------------------
Vulkanizer works with DirectX 9, 10, and 11 games. However, not all games will work on all configurations! It depends on the hardware (the graphics card must support Vulkan) and the specific game engine.

What to do if a game won't launch? (DON'T PANIC)
The script works as safely as possible. Before replacing files, it makes backups (.bak). If after installing Vulkanizer the game throws an error, crashes, or shows a black screen, you do not need to reinstall the game.

Just go to the folder with the game's .exe file and delete the following files:
- d3d9.dll, d3d10core.dll, d3d11.dll, dxgi.dll
- dxvk.conf

Or use the "Uninstall Vulkanizer" button in the program itself. The game will return to its native, clean DirectX state. Nothing will break.

Stability tip: For maximum stability with Vulkan, run games in "Borderless Windowed" mode. This prevents crashes when minimizing (Alt+Tab), eliminates input lag, and ensures stable overlay operation.

----------------------------------------------------------------------
3. SPECIAL INSTRUCTIONS
----------------------------------------------------------------------
[UBISOFT Games (Assassin's Creed, Watch Dogs, Far Cry, etc.)]
The Ubisoft Connect overlay often causes instant crashes when working with Vulkan API. If you are installing Vulkanizer on Ubisoft games, be sure to follow these steps:
1. Open the Ubisoft Connect launcher.
2. Go to Menu -> Settings -> "Interface" tab.
3. Uncheck "Enable in-game overlay for supported games".
4. Launch the game STRICTLY through the Ubisoft Connect launcher itself, not directly via the EXE!

[Ultimate GTA 4 Fix (and old engines)]
Old engines don't know how to work with modern memory capacities. The program has a special toggle: "Emulate top-tier graphics card GTX 680 (VRAM Unlock)".
When enabled:
- The graphics card is spoofed as an NVIDIA GTX 680.
- A hard limit of 4096 MB of video memory is allocated.
- A commandline.txt file is created in the game folder.
- WARNING: Modern Steam/Rockstar launchers ignore files in the folder. The program will copy the necessary parameters to your clipboard (-nomemrestrict -norestrictions -availablevidmem 4096). Be sure to paste them into the game's "Launch Options" in Steam! If you have a pirated version, launch strictly through GTAIV.exe.

----------------------------------------------------------------------
4. SETTINGS AND GRAPHICS PRESETS
----------------------------------------------------------------------
[DXVK Version Selection]
- Latest Version: v2.4+ (Requires Vulkan 1.3 support). Ideal for modern graphics cards.
- Legacy-compatible: v1.10.3 (Requires Vulkan 1.1 support). Specifically for older graphics cards.

[Forced API Selection (Override)]
By default, the program determines the game's API itself. But sometimes games use mixed libraries. You can force the program to install libraries only for DX9, DX10, DX11, or install All at once.

[Optimization Presets (dxvk.conf Generation)]
1. Cinematic Ultra: Maximum smoothness, 4 buffers, 16x anisotropy, extreme LOD detail (-2.0), forced Sample Rate Shading.
2. Ultra Quality: High quality balance, 16x anisotropy, LOD detail (-1.0), 8x tessellation.
3. Best Picture: Clarity and smoothness, FPS priority, 16x anisotropy, medium LOD (-0.5). Optimal choice.
4. Balanced: Optimal visual/FPS ratio, 8x anisotropy, standard LOD (0.0).
5. Pure Vulkan (Vanilla): Only pure DXVK call translation. No graphical enhancements, maximum focus on lowering input lag and high CPU priority.

[Synchronization and Buffering]
MANDATORY: In our presets, vertical synchronization is ENABLED BY DEFAULT via DXVK. Turn off V-Sync in the game's own settings to avoid double input lag!
- V-Sync: ON (Recommended), OFF (Min. delay, screen tearing possible), HALF x2 (for 30/60 fps locks).
- Buffering: Double (2 frames), Triple (3 frames — standard), Quad (4 frames — for ultra-smoothness on powerful PCs).

[Overlay and Monitoring (DXVK HUD)]
- No overlay: Completely disabled.
- Minimal: FPS counter only.
- Extended: FPS, frametime, GPU load, shader compilation, memory.
- Full diagnostic: Displays absolutely all charts, API versions, and pipeline status on screen.

----------------------------------------------------------------------
5. GAME MAINTENANCE TOOLS
----------------------------------------------------------------------
- Clear game cache: Deletes *.dxvk-cache files. Useful if the game starts freezing after driver updates.
- Reset game settings: Finds and deletes config files (GamerProfile.xml, settings.xml, etc.) in Documents and AppData folders.
- Uninstall Vulkanizer: Deep clean. Deletes all DXVK .dll files, dxvk.conf, and restores backups of original Windows files.
- Create shortcut: Creates a direct .lnk shortcut on the desktop to launch the configured game.

----------------------------------------------------------------------
6. GLOBAL OS SYSTEM TWEAKS
----------------------------------------------------------------------
Vulkanizer PRO includes 13 deep operating system optimizations. Requires running as Administrator. All tweaks can be rolled back with a single button "RESET ALL TWEAKS".

1. Unified global DXVK cache: Moves the cache of all games to the C:\DXVK_Cache folder.
2. Windows Game Mode: Forcibly activates suppression of background tasks.
3. Disable Xbox GameDVR: Disables background cyclic screen recording.
4. GPU driver cache cleanup: Cleans NVIDIA/DXCache, AMD/DxCache folders.
5. "Ultimate Performance" power plan: Activates hidden max performance scheme, disables core parking.
6. CPU scheduler priorities: Changes Win32PrioritySeparation to 26, giving max resources to the game.
7. Hardware-Accelerated GPU Scheduling (HAGS): Video memory management bypassing the OS driver.
8. Network stack (MMCSS): Removes network limits, gives games 100% priority.
9. Nagle's algorithm (Low ping): Disables packet buffering (TcpAckFrequency), reducing latency.
10. Clean shutdown (Fast Startup): Disables fast startup/hibernation to clear memory leaks.
11. Disable HPET and timers: Removes micro-freezes during sharp mouse movements.
12. Clean temporary files: Hard cleans Temp and Prefetch directories.
13. Disable Windows transparency: Disables Aero/Fluent effects to save GPU resources.

----------------------------------------------------------------------
7. HOW TO USE
----------------------------------------------------------------------
1. Run the application as Administrator.
2. On the "Games and Settings" tab, click "Scan Steam" or add a game manually.
3. Select a game from the list that appears.
4. Adjust parameters: DXVK version, graphics preset, and overlay.
5. Click "INSTALL VULKANIZER" and wait for libraries to download/extract.
6. Click "Launch Game" (Borderless Windowed mode is recommended).

----------------------------------------------------------------------
8. CONTACTS AND AUTHORS
----------------------------------------------------------------------
Wrapper creators: EvilCat & AI (Golden Standard)
Modification and improvement: Zvezdochka
Creator contact (Telegram): @EvilCat_97
Original DXVK translator project: https://github.com/doitsujin/dxvk

Remember: the chances of encountering a bear with a shotgun are extremely low, but never zero! Enjoy lag-free gaming!
