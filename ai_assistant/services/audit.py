from ..models import AIInteraction


def record_interaction(user, feature, status, output_text='', error_message='', model_name='', **relations):
    return AIInteraction.objects.create(
        user=user,
        feature=feature,
        status=status,
        output_text=output_text,
        error_message=error_message,
        model_name=model_name,
        input_metadata={key: getattr(value, 'pk', value) for key, value in relations.items() if value is not None},
        **relations,
    )
