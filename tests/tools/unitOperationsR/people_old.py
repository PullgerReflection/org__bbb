from pullgerReflection.com_linkedin import api


def add_people(self):
    from pullgerReflection.com_linkedin.tests.tools.DataTemplate import person_data

    pDATA = person_data()
    uuid_new_people = api.add_people(**pDATA)
    self.assertEqual(len(uuid_new_people), 36, "Incorrect uuid new People")
    createdElement = api.get_people(uuid=uuid_new_people)
    for (keyData, valueData) in pDATA.items():
        self.assertEqual(getattr(createdElement, keyData), valueData,
                         f'Incorrect compare DATA on new object in [{keyData}] field: [{getattr(createdElement, keyData)}]<>[{valueData}]')

    return uuid_new_people
