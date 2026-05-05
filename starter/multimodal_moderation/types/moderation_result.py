from pydantic import BaseModel, Field, computed_field


class ModerationResult(BaseModel):
    """
    Base moderation result.

    Holds the fields that are common across every moderation agent
    (text, image, video, audio):
      - rationale: explanation of the moderation decision
      - contains_pii: whether the content contains PII
      - is_unfriendly: whether the tone is unfriendly
      - is_unprofessional: whether the tone is unprofessional

    Subclasses add media-specific fields (e.g. is_disturbing, is_low_quality,
    transcription).

    The ``is_flagged`` computed field returns True if ANY boolean flag on the
    model (including subclass flags) is True, so downstream code can rely on a
    single uniform contract instead of maintaining its own list of "unsafe
    flags".
    """

    rationale: str = Field(description="Explanation of what was harmful and why")

    contains_pii: bool = Field(
        default=False,
        description="Whether the content contains any personally-identifiable information (PII)",
    )
    is_unfriendly: bool = Field(
        default=False,
        description="Whether unfriendly tone or content was detected",
    )
    is_unprofessional: bool = Field(
        default=False,
        description="Whether unprofessional tone or content was detected",
    )

    @computed_field
    @property
    def is_flagged(self) -> bool:
        """True if any boolean moderation flag is set."""
        return any(
            getattr(self, name) is True
            for name, field in self.__class__.model_fields.items()
            if field.annotation is bool
        )


class TextModerationResult(ModerationResult):
    """Text moderation only uses the shared base flags."""

    pass


class ImageModerationResult(ModerationResult):

    is_disturbing: bool = Field(default=False, description="Whether the image is disturbing")
    is_low_quality: bool = Field(default=False, description="Whether the image is low quality")


class VideoModerationResult(ModerationResult):

    is_disturbing: bool = Field(default=False, description="Whether the video is disturbing")
    is_low_quality: bool = Field(default=False, description="Whether the video is low quality")


class AudioModerationResult(ModerationResult):

    transcription: str = Field(description="Transcription of the audio")
