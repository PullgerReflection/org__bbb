
def to_json(self: 'import pullgerReflection.org__bbb.models.models_search'):
    return {
        "id_iso_country": self.city.country.id_iso,
        "id_iso_state": self.city.state.id_iso,
        "id_name_city": self.city.id_name,
        "id_name_category": self.category.id_name
    }
