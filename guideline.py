from __future__ import annotations

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor


class Scene:
    """Base class for interaction scenes."""

    def __init__(self, name: str, manager: "SceneManager") -> None:
        self.name = name
        self.manager = manager

    async def enter(self) -> None:
        """Called when the scene becomes active."""

    async def exit(self) -> None:
        """Called when the scene is no longer active."""

    async def handle_message(self, message: types.Message) -> bool:
        """Handle an incoming Telegram message."""
        return False

    async def request_transition(self, scene_name: str) -> None:
        """Ask the manager to activate another scene."""
        await self.manager.transition_to(scene_name)


class SceneManager:
    """Controls which scene is active, similar to Unity's SceneManager."""

    def __init__(self) -> None:
        self._scenes: dict[str, Scene] = {}
        self._active_scene: Scene | None = None

    def register(self, scene: Scene) -> None:
        self._scenes[scene.name] = scene

    async def transition_to(self, name: str) -> None:
        if name not in self._scenes:
            raise ValueError(f"Scene '{name}' is not registered")
        if self._active_scene is self._scenes[name]:
            return
        if self._active_scene:
            await self._active_scene.exit()
        self._active_scene = self._scenes[name]
        await self._active_scene.enter()

    async def handle_message(self, message: types.Message) -> bool:
        if not self._active_scene:
            return False
        return await self._active_scene.handle_message(message)


class MainMenu(Scene):
    async def enter(self) -> None:
        # Could preload menu keyboards or content here
        print("Активирована сцена главного меню")

    async def handle_message(self, message: types.Message) -> bool:
        if message.text == "/start":
            await message.answer("Показать главное меню")
            return True
        if message.text == "/settings":
            await message.answer("Переключаюсь на настройки")
            await self.request_transition("settings")
            return True
        return False


class Settings(Scene):
    async def enter(self) -> None:
        print("Активирована сцена настроек")

    async def handle_message(self, message: types.Message) -> bool:
        if message.text == "/settings":
            await message.answer("Открыли настройки")
            return True
        if message.text == "/back":
            await message.answer("Возврат в главное меню")
            await self.request_transition("menu")
            return True
        return False


bot = Bot("TOKEN")
dp = Dispatcher(bot)
scene_manager = SceneManager()
scene_manager.register(MainMenu("menu", scene_manager))
scene_manager.register(Settings("settings", scene_manager))


async def on_startup(dispatcher: Dispatcher) -> None:
    await scene_manager.transition_to("menu")


@dp.message_handler()
async def on_message(message: types.Message) -> None:
    handled = await scene_manager.handle_message(message)
    if not handled:
        await message.answer("Не понял команду.")


executor.start_polling(dp, on_startup=on_startup)
