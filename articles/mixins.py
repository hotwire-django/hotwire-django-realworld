from django.core.exceptions import PermissionDenied


class UserIsAuthorMixin(object):
    """
    Checks that the user is the author of the object. If they are not, raise a
    403 error
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.profile.pk is not self.get_object().author.pk:
            raise PermissionDenied

        return super(UserIsAuthorMixin, self).dispatch(request, *args, **kwargs)
