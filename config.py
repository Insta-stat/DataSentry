# INSTAGRAM REEL SCRAPPER SETTINGS
INST_REAL_SCRAPER_ACTOR_ID = 'xMc5Ga1oCONPmWJIa'

# Настройки анализа аккаунтов
reels_input_data = {
    "username": ['johnkeeganlifestyle'],  # Список аккаунтов для анализа
    "resultsLimit": 5,          # Максимальное количество результатов
    "scrapePosts": False,         # Анализировать посты
    "scrapeReels": True,          # Анализировать reels
    "scrapeStories": False        # Анализировать stories
}

def save_config():
    """Сохраняет текущую конфигурацию в файл"""
    import traceback
    
    try:
        # Создаем бэкап текущего файла
        with open(__file__, 'r') as f:
            original_content = f.read()
        
        with open(__file__ + '.bak', 'w') as f:
            f.write(original_content)
        
        # Проверяем значения перед сохранением
        if not isinstance(reels_input_data.get("username"), list):
            raise ValueError(f"username должен быть списком, получено: {type(reels_input_data.get('username'))}")
        
        if not isinstance(reels_input_data.get("resultsLimit"), (int, float)):
            raise ValueError(f"resultsLimit должен быть числом, получено: {type(reels_input_data.get('resultsLimit'))}")
        
        results_limit = int(reels_input_data["resultsLimit"])
        if results_limit < 1 or results_limit > 500:
            raise ValueError(f"resultsLimit должен быть от 1 до 500, получено: {results_limit}")
        
        # Находим начало и конец блока конфигурации
        lines = original_content.split('\n')
        config_start = -1
        config_end = -1
        
        for i, line in enumerate(lines):
            if line.strip() == 'reels_input_data = {':
                config_start = i
            elif config_start >= 0 and line.strip() == '}':
                config_end = i
                break
        
        if config_start == -1 or config_end == -1:
            raise ValueError("Не удалось найти блок конфигурации в файле")
        
        # Создаем новый блок конфигурации
        new_config = [
            'reels_input_data = {',
            f'    "username": {reels_input_data["username"]},  # Список аккаунтов для анализа',
            f'    "resultsLimit": {results_limit},          # Максимальное количество результатов',
            '    "scrapePosts": False,         # Анализировать посты',
            '    "scrapeReels": True,          # Анализировать reels',
            '    "scrapeStories": False        # Анализировать stories',
            '}'
        ]
        
        # Заменяем старый блок конфигурации на новый
        new_content = '\n'.join(lines[:config_start] + new_config + lines[config_end + 1:])
        
        # Проверяем, что новый контент валидный Python код
        try:
            compile(new_content, __file__, 'exec')
        except SyntaxError as se:
            raise ValueError(f"Новая конфигурация содержит синтаксические ошибки: {str(se)}")
        
        # Сохраняем обновленный контент
        with open(__file__, 'w') as f:
            f.write(new_content)
            
    except Exception as e:
        # В случае ошибки восстанавливаем из бэкапа
        error_details = f"Ошибка: {str(e)}\n\nТекущие значения:\n"
        error_details += f"username: {reels_input_data.get('username')} ({type(reels_input_data.get('username'))})\n"
        error_details += f"resultsLimit: {reels_input_data.get('resultsLimit')} ({type(reels_input_data.get('resultsLimit'))})\n"
        error_details += f"\nПолный стек ошибки:\n{traceback.format_exc()}"
        
        try:
            import os
            if os.path.exists(__file__ + '.bak'):
                with open(__file__ + '.bak', 'r') as f:
                    backup_content = f.read()
                with open(__file__, 'w') as f:
                    f.write(backup_content)
                error_details += "\n\nКонфигурация восстановлена из бэкапа."
        except Exception as restore_error:
            error_details += f"\n\nОшибка при восстановлении из бэкапа: {str(restore_error)}"
        
        raise ValueError(error_details)

def update_accounts(accounts, results_limit=None):
    """Обновляет настройки анализа и сохраняет их в файл
    
    Args:
        accounts (list): Список аккаунтов для анализа
        results_limit (int, optional): Количество последних постов для анализа
    """
    global reels_input_data
    reels_input_data["username"] = accounts
    if results_limit is not None:
        reels_input_data["resultsLimit"] = results_limit
    
    # Сохраняем изменения в файл
    save_config()

stdev_hot_treshold = 2
stdev_very_successful_treshold = 0.75

def z_categorize(z):
    if z > 2.0:
        return '🔥viral hit'
    elif z > 1.0:
        return '✅very successful'
    elif z > 0.2:
        return 'successful'
    elif z >= -1.0:
        return 'average'
    else:
        return 'weak'

top_reels_count = 15
bad_reels_count = 5
