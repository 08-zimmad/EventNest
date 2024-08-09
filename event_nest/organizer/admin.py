from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import EventNestUsers, Events


class EventNestUsersCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
        )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput
        )

    class Meta:
        model = EventNestUsers
        fields = ('email', 'role', 'organization')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class EventNestUsersChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = EventNestUsers
        fields = (
            'username',
            'email',
            'password',
            'organization',
            'role',
            'is_active',
            'is_staff'
            )


class EventNestUsersAdmin(BaseUserAdmin):
    form = EventNestUsersChangeForm
    add_form = EventNestUsersCreationForm

    list_display = ('username', 'email', 'is_staff', 'is_active', 'role')
    list_filter = ('is_staff', 'is_active', 'role')
    fieldsets = (
        (None, {
                'fields': ('username', 'email', 'password', 'organization', 'role')
            }),
        ('Permissions', {
             'fields': ('is_staff', 'is_active')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': (
                'email',
                'password1',
                'password2',
                'organization',
                'role'
                )
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(EventNestUsers, EventNestUsersAdmin)
admin.site.register(Events)
