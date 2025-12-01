from django import forms
from user_accounts.models import User


class UserSignupForm(forms.ModelForm):
    confirm_password = forms.CharField(
        max_length=100,
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                     'focus:ring-2 focus:ring-blue-500 focus:outline-none'
        })
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username','email','profile_pic','password','confirm_password']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'Email',
            'profile_pic': 'Prfile Picture',
            'password': 'Password',
            'confirm_password': 'Confirm Password',
        }

        error_messages = {
            'first_name' : {'required' : 'First Name is required field.'},
            'last_name' : {'required' : 'Last Name is required field.'},
            'username' : {'required': 'Username is required field.'},
            'email' : {'required' : 'Email is required field.','invalid' :'Please enter a valid email address.'},
            'password' : {'required': 'Password is required field.'},
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
            'username': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
            'profile_pic': forms.FileInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'The confirmation password does not match the password. Please try again.')

        return cleaned_data
    

    def save(self, commit=True):
        cleaned_data = self.cleaned_data

        user = User.objects.create_user(
            email=cleaned_data.get("email"),
            username=cleaned_data.get("username"),
            password=cleaned_data.get("password"),
            first_name=cleaned_data.get("first_name"),
            last_name=cleaned_data.get("last_name"),
            profile_pic=cleaned_data.get("profile_pic"),
        )

        return user    
    

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
        error_messages={
        'required': 'Email is required.',
        'invalid': 'Please enter a valid email address.',
        }

    )
    password = forms.CharField(
        max_length=100,
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                     'focus:ring-2 focus:ring-blue-500 focus:outline-none'
        }),
        error_messages={'required' : 'Password is required field.'}

    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'profile_pic']
        labels = {
            'first_name' : 'First Name',
            'last_name' : 'Last Name',
            'username' : 'Username',
            'email' : 'Email',
            'profile_pic' : 'Profile Picture'
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
            'username': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:ring-2 focus:ring-blue-500 focus:outline-none',
                'readonly': 'readonly'              
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:ring-2 focus:ring-blue-500 focus:outline-none',
                'readonly': 'readonly'              
            }),
            'profile_pic': forms.FileInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        if self.instance:
            cleaned_data['username'] = self.instance.username
            cleaned_data['email'] = self.instance.email
        return cleaned_data    


class UserChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        max_length=100,
        label="Current Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                     'focus:ring-2 focus:ring-blue-500 focus:outline-none'
        }),
        error_messages = {'required' : 'This field is required.'},
        required=True
    )
    new_password = forms.CharField(
        max_length=100,
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                     'focus:ring-2 focus:ring-blue-500 focus:outline-none'
        }),
        error_messages = {'required' : 'This field is required.'}
    )
    confirm_new_password = forms.CharField(
        max_length=100,
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                     'focus:ring-2 focus:ring-blue-500 focus:outline-none'
        }),
        error_messages = {'required' : 'This field is required.'}
    )
