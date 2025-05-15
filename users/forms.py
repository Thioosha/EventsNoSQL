from django import forms

ACCOUNT_CHOICES = (
    ('organizer', 'Je veux organiser des événements'),
    ('participant', 'Je veux seulement participer'),
)

class AccountTypeForm(forms.Form):
    account_type = forms.ChoiceField(
        choices=ACCOUNT_CHOICES,
        widget=forms.RadioSelect,
        label="Quel type de compte veux-tu créer ?"
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    full_name = forms.CharField(
        max_length=100,
        label="Nom complet",
        widget=forms.TextInput(attrs={'placeholder': 'Nom complet'})
    )
    email = forms.EmailField(
        label="Adresse mail",
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
        label="Mot de passe"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmez le mot de passe'}),
        label="Confirmez le mot de passe"
    )

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        confirm_pwd = cleaned_data.get('confirm_password')

        if pwd and confirm_pwd and pwd != confirm_pwd:
            self.add_error('confirm_password', "Les mots de passe ne correspondent pas.")

        return cleaned_data

