from registration.forms import RegistrationForm
from captcha.fields import ReCaptchaField

class UserRegistrationForm(RegistrationForm):
  captcha = ReCaptchaField(attrs={'theme':'clean'})
