# This file contains the Pydantic models, used to define the structure and
# validation of data exchanged between API and client.

from pydantic import BaseModel


# Define Pydantic model for token response.
class Token(BaseModel):
  access_token: str
  token_type: str


