import os
import subprocess
from datetime import datetime


class GitHubDeployer:
    def __init__(self, repo_path, remote_url, branch="main"):
        self.repo_path = repo_path  # Локальный путь к репозиторию
        self.remote_url = remote_url  # Ссылка на удалённый репозиторий
        self.branch = branch  # Ветка, куда будут отправляться изменения

    def run_git_command(self, *args):
        """
        Выполняет команду Git в указанной директории и возвращает вывод.
        """
        result = subprocess.run(
            ["git", *args],
            cwd=self.repo_path,
            text=True,
            capture_output=True
        )
        if result.returncode != 0:
            raise Exception(f"Ошибка выполнения git команды: {result.stderr}")
        return result.stdout.strip()

    def initialize_repo(self):
        """
        Инициализирует репозиторий, если он ещё не инициализирован.
        """
        if not os.path.exists(os.path.join(self.repo_path, ".git")):
            print("Инициализация Git репозитория...")
            self.run_git_command("init")
            self.run_git_command("remote", "add", "origin", self.remote_url)
        else:
            print("Git репозиторий уже инициализирован.")

    def create_branch(self):
        """
        Проверяет и создаёт ветку, если она не существует.
        """
        try:
            self.run_git_command("checkout", "-b", self.branch)
        except Exception as e:
            print(f"Ветка {self.branch} уже существует или не может быть создана. {e}")

    def add_all_files(self):
        """
        Добавляет все файлы в индекс для коммита.
        """
        print("Добавление всех файлов...")
        self.run_git_command("add", ".")

    def has_changes(self):
        """
        Проверяет, есть ли изменения в рабочем каталоге.
        """
        status = self.run_git_command("status", "--porcelain")
        return bool(status.strip())

    def commit_changes(self, message):
        """
        Создаёт коммит с указанным сообщением.
        """
        print("Создание коммита...")
        self.run_git_command("commit", "-m", message)

    def push_changes(self):
        """
        Отправляет изменения в удалённый репозиторий.
        """
        print("Отправка изменений в репозиторий...")
        self.run_git_command("push", "-u", "origin", self.branch)

    def deploy(self, commit_message=None):
        """
        Основной процесс деплоя: добавление файлов, коммит и пуш.
        """
        try:
            self.initialize_repo()  # Инициализация репозитория, если нужно
            self.create_branch()  # Создание ветки, если она отсутствует
            self.add_all_files()  # Добавление всех файлов в индекс

            if not self.has_changes():  # Проверка, есть ли изменения
                print("Нет изменений для коммита.")
                return

            # Установка сообщения коммита
            if commit_message is None:
                commit_message = f"Автообновление: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            self.commit_changes(commit_message)  # Создание коммита
            self.push_changes()  # Отправка изменений на GitHub
            print("Обновление успешно отправлено на GitHub!")
        except Exception as e:
            print(f"Ошибка деплоя: {e}")


if __name__ == "__main__":
    # Укажите путь к вашему проекту
    repo_path = "C:\\Users\\vovawe\\PycharmProjects\\pythonProject5"

    # Укажите ваш удалённый репозиторий
    remote_url = "https://github.com/vovanChikssszs/vovawe-chat.git"

    # Ветка для пуша
    branch = "main"

    # Создание и запуск деплоя
    deployer = GitHubDeployer(repo_path, remote_url, branch)
    deployer.deploy("Обновление чата: улучшения и исправления")
