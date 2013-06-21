class NamedModel(db.Model):
    """A Model subclass for entities which automatically generate their own key
    names on creation. See documentation for _generate_key function for
    requirements."""

    def __init__(self, *args, **kwargs):
        # kwargs['key_name'] = kwargs['name']
        kwargs['key_name'] = _generate_key(self, kwargs)
        super(NamedModel, self).__init__(*args, **kwargs)


def _generate_key(entity, kwargs):
    """Generates a key name for the given entity, which was constructed with
    the given keyword args.  The entity must have a KEY_NAME property, which
    can either be a string or a callable.

    If KEY_NAME is a string, the keyword args are interpolated into it.  If
    it's a callable, it is called, with the keyword args passed to it as a
    single dict."""

    # Make sure the class has its KEY_NAME property set
    if not hasattr(entity, 'KEY_NAME'):
        raise RuntimeError, '%s entity missing KEY_NAME property' % (
            entity.entity_type())

    # Make a copy of the kwargs dict, so any modifications down the line don't
    # hurt anything
    kwargs = dict(kwargs)

    # The KEY_NAME must either be a callable or a string.  If it's a callable,
    # we call it with the given keyword args.
    if callable(entity.KEY_NAME):
        return entity.KEY_NAME(kwargs)

    # If it's a string, we just interpolate the keyword args into the string,
    # ensuring that this results in a different string.
    elif isinstance(entity.KEY_NAME, basestring):
        # Try to create the key name, catching any key errors arising from the
        # string interpolation
        try:
            key_name = entity.KEY_NAME % kwargs
        except KeyError:
            raise RuntimeError, 'Missing keys required by %s entity\'s KEY_NAME '\
                'property (got %r)' % (entity.entity_type(), kwargs)

        # Make sure the generated key name is actually different from the
        # template
        if key_name == entity.KEY_NAME:
            raise RuntimeError, 'Key name generated for %s entity is same as '\
                'KEY_NAME template' % entity.entity_type()

        return key_name

    # Otherwise, the KEY_NAME is invalid
    else:
        raise TypeError, 'KEY_NAME of %s must be a string or callable' % (
            entity.entity_type())



class Foo(NamedModel):
    KEY_NAME = '%(name)s'
    name = db.StringProperty()
