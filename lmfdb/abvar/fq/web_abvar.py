# -*- coding: utf-8 -*-
import re
from flask import url_for

from lmfdb.base import getDBConnection
from lmfdb.WebNumberField import WebNumberField, nf_display_knowl
from lmfdb.transitive_group import group_display_knowl

lmfdb_label_regex = re.compile(r'(\d+)\.(\d+)\.([a-z_]+)')

def split_label(lab):
    return lmfdb_label_regex.match(lab).groups()

def av_display_knowl(label):
    return '<a title = "[av.data]" knowl="av.fq.abvar.data" kwargs="label=' + str(label) + '">' + label + '</a>'
    
def av_data(label):
    C = getDBConnection()
    abvar = C.abvar.fq_isog.find_one({ 'label' : label })
    wnf = WebNumberField(abvar['number_field'])
    inf = '<div>Dimension: ' + str(abvar['g']) + '<br />'
    if not wnf.is_null():
        inf += 'Number field: ' + nf_display_knowl(abvar['number_field'], C, name = abvar['number_field']) + '<br />'
        inf += 'Galois group: ' + group_display_knowl(abvar['galois_n'],abvar['galois_t'],C) + '<br />'
    inf += '$p$-rank: ' + str(abvar['p_rank']) + '</div>'
    inf += '<div align="right">'
    g, q, iso = split_label(label)
    url = url_for("abvarfq.abelian_varieties_by_gqi", g = g, q = q, iso = iso)
    inf += '<a href="%s">%s home page</a>' % (url, label)
    inf += '</div>'
    return inf
