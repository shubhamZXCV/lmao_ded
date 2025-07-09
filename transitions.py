from moviepy.decorators import add_mask_if_none, requires_duration
from moviepy.video.fx import CrossFadeIn, CrossFadeOut, SlideIn, SlideOut

__all__ = ["crossfadein", "crossfadeout", "slide_in", "slide_out"]

@requires_duration
@add_mask_if_none
def crossfadein(clip, duration):
    clip.mask.duration = clip.duration
    return clip.with_effects([CrossFadeIn(duration)])

@requires_duration
@add_mask_if_none
def crossfadeout(clip, duration):
    clip.mask.duration = clip.duration
    return clip.with_effects([CrossFadeOut(duration)])

def slide_in(clip, duration, side):
    return clip.with_effects([SlideIn(duration, side)])

@requires_duration
def slide_out(clip, duration, side):
    return clip.with_effects([SlideOut(duration, side)])
