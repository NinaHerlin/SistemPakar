def cf_from_mb_md(mb, md):
    return mb - md

def combine_cf(cf1, cf2):
    return cf1 + cf2 * (1 - cf1)
