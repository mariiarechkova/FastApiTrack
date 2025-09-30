class OrganisationNotFoundError(Exception):
    def __init__(self, org_id: int):
        super().__init__(f"Organisation {org_id} not found")
        self.org_id = org_id