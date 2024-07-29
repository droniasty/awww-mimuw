from django import forms


class StandardForm(forms.Form):
    standard = forms.ChoiceField(choices=[('c89', 'c89'), ('c99', 'c99'), ('c11', 'c11')])

class OptimizationForm(forms.Form):
    optimization = forms.ChoiceField(choices=[('--nogcse', '--nogcse'), ('--opt-code-speed', '--opt-code-speed'), ('--opt-code-size', '--opt-code-size'), ('--allow-unsafe-read', '--allow-unsafe-read')])

class ProcessorForm(forms.Form):
    processor = forms.ChoiceField(choices=[('MCS51','MCS51'),('STM8','STM8'),('Z80','Z80')])




    