from django import forms

CATEGORY_CHOICES = [
    ('Musique', 'Musique'),
    ('Art', 'Art'),
    ('Conférence', 'Conférence'),
    ('Sport', 'Sport'),
    ('Atelier', 'Atelier'),
    ('Formation', 'Formation'),
    ('Technologie', 'Technologie'),
    ('Rencontre', 'Rencontre'),
    ('Mode', 'Mode'),
    ('Santé', 'Santé'),
    ('Voyage', 'Voyage'),
    ('Cinéma', 'Cinéma'),
    ('Théâtre', 'Théâtre'),
    ('Danse', 'Danse'),
    ('Gaming', 'Gaming'),
    ('Littérature', 'Littérature'),
    ('Religion', 'Religion'),
    ('Cuisine', 'Cuisine'),
    ('Networking', 'Networking'),
    ('Autre', 'Autre'),
]

class MongoEventForm(forms.Form):
    title = forms.CharField(label="Titre")
    description = forms.CharField(widget=forms.Textarea, required=False)
    location = forms.CharField(label="Lieu")
    start_datetime = forms.DateTimeField(
        label="Date et heure de début",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    end_datetime = forms.DateTimeField(
        label="Date et heure de fin",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    image = forms.ImageField(label="Image de l'événement", required=False)


    total_slots = forms.IntegerField(label="Nombre total de places")
    available_slots = forms.IntegerField(label="Places disponibles")
    price = forms.FloatField(label="Prix", initial=0.0)
    
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        label="Catégorie"
    )

    def clean(self):
        cleaned_data = super().clean()
        total = cleaned_data.get("total_slots")
        available = cleaned_data.get("available_slots")
        if total is not None and available is not None and available > total:
            self.add_error("available_slots", "Les places dispos doivent pas dépasser le total.")
        return cleaned_data


