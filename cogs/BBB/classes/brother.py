import unicodedata


class Brother:
  def __init__(self, id, name, avatar):
    self.id = id
    self.name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8').strip()
    self.avatar = avatar

  def __repr__(self) -> str:
    return f"Brother({self.name}, {self.id}, {self.avatar})"
