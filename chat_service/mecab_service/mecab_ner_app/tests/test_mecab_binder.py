from pathlib import Path

from app.controller.service.bert_sender import get_mecab_bind_feature
from app.controller.service.mecab_binder import MecabEntity, MecabIntent, MecabBinder
from app.domain.mecab_domain import BindResult, BindInfo
from chat_service.chat_core.chat_domain import MecabBertBindFeature, MecabFeature, MecabSimpleFeature
from domain.mecab_domain import Category, MecabNerFeature


def test_mecab_ner_simple():
    entity_path = Path(__file__).resolve().parent.parent.joinpath("data", "entities", "entity_data")
    m_e = MecabEntity(ner_path=str(entity_path), clear_mecab_dir=False)
    intent_path = Path(__file__).resolve().parent.parent.joinpath("data", "intents", "intent_data")
    m_i = MecabIntent(ner_path=str(intent_path), clear_mecab_dir=False, infer=False)

    test_sentence = "진주 아이유 듣는 것이 좋다 아이묭 듣는 것이 좋다"

    m_e_parse = m_e.parse(test_sentence)
    assert m_e_parse == [('진주 아이유', MecabNerFeature(word='진주 아이유', pos='entity', start_idx=0, end_idx=2, category=Category(large='music_singer', small='가수'))), ('듣', MecabNerFeature(word='듣', pos='VV', start_idx=2, end_idx=2, category=None)), ('는', MecabNerFeature(word='는', pos='ETM', start_idx=3, end_idx=3, category=None)), ('것', MecabNerFeature(word='것', pos='NNB', start_idx=4, end_idx=4, category=None)), ('이', MecabNerFeature(word='이', pos='JKS', start_idx=5, end_idx=5, category=None)), ('좋', MecabNerFeature(word='좋', pos='VA', start_idx=6, end_idx=6, category=None)), ('다', MecabNerFeature(word='다', pos='EF', start_idx=7, end_idx=7, category=None)), ('아이묭', MecabNerFeature(word='아이묭', pos='entity', start_idx=8, end_idx=10, category=Category(large='music_singer', small='가수'))), ('듣', MecabNerFeature(word='듣', pos='VV', start_idx=10, end_idx=10, category=None)), ('는', MecabNerFeature(word='는', pos='ETM', start_idx=11, end_idx=11, category=None)), ('것', MecabNerFeature(word='것', pos='NNB', start_idx=12, end_idx=12, category=None)), ('이', MecabNerFeature(word='이', pos='JKS', start_idx=13, end_idx=13, category=None)), ('좋', MecabNerFeature(word='좋', pos='VA', start_idx=14, end_idx=14, category=None)), ('다', MecabNerFeature(word='다', pos='EC', start_idx=15, end_idx=15, category=None))]

    m_e_mor = m_e.morphs(test_sentence)
    assert m_e_mor == ['진주 아이유', '듣', '는', '것', '이', '좋', '다', '아이묭', '듣', '는', '것', '이', '좋', '다']
    m_e_ner = m_e.ners(test_sentence)
    assert m_e_ner == [MecabNerFeature(word='진주 아이유', pos='entity', start_idx=0, end_idx=2, category=Category(large='music_singer', small='가수')), MecabNerFeature(word='아이묭', pos='entity', start_idx=8, end_idx=10, category=Category(large='music_singer', small='가수'))]


    test_sentence = "진주 아이유 듣는 것이 좋다 아이묭 듣는 것이 좋다"

    m_i_parse = m_i.parse(test_sentence)
    assert m_i_parse == [('진주', MecabNerFeature(word='진주', pos='NNG', start_idx=0, end_idx=0, category=None)), ('아이유', MecabNerFeature(word='아이유', pos='NNG', start_idx=1, end_idx=1, category=None)), ('듣는 것이 좋다', MecabNerFeature(word='듣는 것이 좋다', pos='intent', start_idx=2, end_idx=8, category=Category(large='music_like', small='듣는게 좋다'))), ('아이', MecabNerFeature(word='아이', pos='IC', start_idx=8, end_idx=8, category=None)), ('묭', MecabNerFeature(word='묭', pos='UNKNOWN', start_idx=9, end_idx=9, category=None)), ('듣는 것이 좋다', MecabNerFeature(word='듣는 것이 좋다', pos='intent', start_idx=10, end_idx=16, category=Category(large='music_like', small='듣는게 좋다')))]

    m_i_morph = m_i.morphs(test_sentence)
    assert m_i_morph == ['진주', '아이유', '듣는 것이 좋다', '아이', '묭', '듣는 것이 좋다']

    m_i_ners = m_i.ners(test_sentence)
    assert m_i_ners == [MecabNerFeature(word='듣는 것이 좋다', pos='intent', start_idx=2, end_idx=8, category=Category(large='music_like', small='듣는게 좋다')), MecabNerFeature(word='듣는 것이 좋다', pos='intent', start_idx=10, end_idx=16, category=Category(large='music_like', small='듣는게 좋다'))]


def test_get_bind():
    entity_path = Path(__file__).resolve().parent.parent.joinpath("data", "entities", "entity_data")
    intent_path = Path(__file__).resolve().parent.parent.joinpath("data", "intents", "intent_data")

    m_b = MecabBinder(entity_path=str(entity_path), intent_path=str(intent_path))
    test_sentence = "동대문에서 진주 아이유 듣는 것이 좋다 아이묭 듣는 것이 좋다"
    bind_result = m_b.get_bind(test_sentence)

    assert bind_result == BindResult(bind_list=[BindInfo(bind_category='music', entity=MecabNerFeature(word='진주 아이유', pos='entity', start_idx=3, end_idx=5, category=Category(large='music_singer', small='가수')), intent=MecabNerFeature(word='듣는 것이 좋다', pos='intent', start_idx=5, end_idx=11, category=Category(large='music_like', small='듣는게 좋다')), end_idx=11, split_sentence=None), BindInfo(bind_category='music', entity=MecabNerFeature(word='아이묭', pos='entity', start_idx=11, end_idx=13, category=Category(large='music_singer', small='가수')), intent=MecabNerFeature(word='듣는 것이 좋다', pos='intent', start_idx=13, end_idx=19, category=Category(large='music_like', small='듣는게 좋다')), end_idx=19, split_sentence=None)], intent_list=[], entity_list=[], noun_list=[MecabNerFeature(word='동', pos='NNP', start_idx=0, end_idx=0, category=None), MecabNerFeature(word='대문', pos='NNP', start_idx=1, end_idx=1, category=None), MecabNerFeature(word='것', pos='NNB', start_idx=7, end_idx=7, category=None), MecabNerFeature(word='것', pos='NNB', start_idx=15, end_idx=15, category=None)])

    multi_en_in = m_b.split_multi_en_in(test_sentence, bind_result.bind_list)

    assert multi_en_in == [BindInfo(bind_category='music', entity=MecabNerFeature(word='진주 아이유', pos='entity', start_idx=3, end_idx=5, category=Category(large='music_singer', small='가수')), intent=MecabNerFeature(word='듣는 것이 좋다', pos='intent', start_idx=5, end_idx=11, category=Category(large='music_like', small='듣는게 좋다')), end_idx=11, split_sentence='동대문에서 진주 아이유 듣는 것이 좋다'), BindInfo(bind_category='music', entity=MecabNerFeature(word='아이묭', pos='entity', start_idx=11, end_idx=13, category=Category(large='music_singer', small='가수')), intent=MecabNerFeature(word='듣는 것이 좋다', pos='intent', start_idx=13, end_idx=19, category=Category(large='music_like', small='듣는게 좋다')), end_idx=19, split_sentence='아이묭 듣는 것이 좋다')]


def test_bert_send():
    entity_path = Path(__file__).resolve().parent.parent.joinpath("data", "entities", "entity_data")
    intent_path = Path(__file__).resolve().parent.parent.joinpath("data", "intents", "intent_data")

    m_b = MecabBinder(entity_path=str(entity_path), intent_path=str(intent_path))
    sentence = "치킨이랑 진주 아이유 듣는 것이 좋다 아이묭 좋아해 동대문 좋아"
    value = get_mecab_bind_feature(sentence=sentence, mecab_binder=m_b)
    m_b_d_list, entity_list, intent_list = value
    assert m_b_d_list == [MecabBertBindFeature(bind_category='music', bind_sentence='진주 아이유 듣는 것이 좋다', entity=MecabFeature(value='진주 아이유', large_category='music_singer', small_category='가수'), intent=MecabFeature(value='듣는 것이 좋다', large_category='music_like', small_category='듣는게 좋다'), bert_confirm=False), MecabBertBindFeature(bind_category='music', bind_sentence='아이묭 좋아해', entity=MecabFeature(value='아이묭', large_category='music_singer', small_category='가수'), intent=MecabFeature(value='좋아해', large_category='music_like', small_category='좋다'), bert_confirm=False)]
    assert entity_list == [MecabSimpleFeature(value='치킨', large_category='fastfood', small_category='fastfood', user_sentence='치킨이랑 진주 아이유 듣는 것이 좋다 아이묭 좋아해 동대문 좋아', bert_confirm=False)]
    assert intent_list == []

    value = get_mecab_bind_feature(sentence=sentence, mecab_binder=m_b, intent_category=["food_like"])
    m_b_d_list, entity_list, intent_list = value
    assert m_b_d_list == [MecabBertBindFeature(bind_category='music', bind_sentence='진주 아이유 듣는 것이 좋다', entity=MecabFeature(value='진주 아이유', large_category='music_singer', small_category='가수'), intent=MecabFeature(value='듣는 것이 좋다', large_category='music_like', small_category='듣는게 좋다'), bert_confirm=False), MecabBertBindFeature(bind_category='music', bind_sentence='아이묭 좋아해', entity=MecabFeature(value='아이묭', large_category='music_singer', small_category='가수'), intent=MecabFeature(value='좋아해', large_category='music_like', small_category='좋다'), bert_confirm=False)]
    assert entity_list == [MecabSimpleFeature(value='치킨', large_category='fastfood', small_category='fastfood', user_sentence='치킨이랑 진주 아이유 듣는 것이 좋다 아이묭 좋아해 동대문 좋아', bert_confirm=False)]
    assert intent_list == [MecabSimpleFeature(value='좋아해', large_category='food_like', small_category='좋다', user_sentence='치킨이랑 진주 아이유 듣는 것이 좋다 아이묭 좋아해 동대문 좋아', bert_confirm=False), MecabSimpleFeature(value='좋아해', large_category='food_like', small_category='좋아한다', user_sentence='치킨이랑 진주 아이유 듣는 것이 좋다 아이묭 좋아해 동대문 좋아', bert_confirm=False), MecabSimpleFeature(value='좋', large_category='food_like', small_category='좋다', user_sentence='치킨이랑 진주 아이유 듣는 것이 좋다 아이묭 좋아해 동대문 좋아', bert_confirm=False)]
