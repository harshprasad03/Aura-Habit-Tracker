
import customtkinter as ctk
from pages.dashboard import DashboardPage
from pages.habits import HabitsPage
from pages.analytics import AnalyticsPage
from pages.character import CharacterPage
from components.sidebar import NavigationSidebar
from components.header import AppHeader
from components.background import AnimatedBackground
from components.achievements import AchievementSystem
from components.level_system import LevelSystem
from styles.themes import apply_modern_theme
from data_handler import load_data

class AuraHabitTracker(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aura Farmer ⚡")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        apply_modern_theme()
        self.data = load_data()
        self.achievement_system = AchievementSystem()
        self.level_system = LevelSystem()
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.setup_ui()
        
    def setup_ui(self):
 
        self.header = AppHeader(self, switch_callback=self.toggle_theme)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        

        self.sidebar = NavigationSidebar(self, self.switch_page)
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        

        self.main_container = ctk.CTkFrame(self, corner_radius=10)
        self.main_container.grid(row=1, column=1, sticky="nsew", padx=(0, 10), pady=10)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        
        self.pages = {
            "dashboard": DashboardPage(self.main_container, self.data),
            "habits": HabitsPage(self.main_container, self.data),
            "analytics": AnalyticsPage(self.main_container, self.data),
            "character": CharacterPage(self.main_container, self.data)
        }
        
        
        self.current_page = "dashboard"
        self.show_page("dashboard")
    
    def show_page(self, page_name):
        
        for page in self.pages.values():
            page.grid_forget()
        
        
        self.pages[page_name].grid(row=0, column=0, sticky="nsew")
        self.current_page = page_name
        self.sidebar.set_active_page(page_name)
        self.sidebar.update_aura_points(self.data.get("aura_points", 0))
    
    def switch_page(self, page_name):
        self.show_page(page_name)
    
    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        new_mode = "Light" if current == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        self.header.update_theme_button(new_mode)

if __name__ == "__main__":
    app = AuraHabitTracker()
    app.mainloop()