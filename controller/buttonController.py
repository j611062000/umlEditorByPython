class ButtonController():

    availableButtons    = list()
    currentActiveButton = None

    @classmethod
    def knwoWhatAreAvailableButtons(cls, available_buttons):
        cls.availableButtons = available_buttons
    
    @classmethod
    def knwoWhatIsCurrentActiveButton(cls, current_active_button):
        cls.currentActiveButton = current_active_button
    
    @classmethod
    def deactivateUnnecessaryButtons(cls):
        for button in cls.availableButtons:
            if button.nameOfButton != cls.currentActiveButton:
                button.configure(background = "grey", fg = "black")
