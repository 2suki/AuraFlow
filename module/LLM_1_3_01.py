import re
import requests
import json
import time

# 添加地点变量（在文件开头）
CURRENT_PROVINCE = "广东"  # 在这里设置省份

# 心理健康热线数据库
MENTAL_HEALTH_HOTLINES = {
    "全国": {
        "青少年法律与心理咨询热线": "12355",
        "全国青少年心理健康专线": "4000-100-525",
        "全国心理援助热线": "400-161-9995",
        "服务时间": "24小时"
    },
    "北京": {
        "北京市心理援助热线": "010-82951332",
        "北京心理危机干预中心": "010-62715275",
        "青少年法律与心理咨询热线": "12355",
        "全国青少年心理健康专线": "4000-100-525",
        "服务时间": "24小时"
    },
    "上海": {
        "上海市心理援助热线": "021-12320-5",
        "上海青少年公共服务平台": "12355",
        "青少年法律与心理咨询热线": "12355",
        "全国青少年心理健康专线": "4000-100-525",
        "服务时间": "24小时"
    },
    "广东": {
        "广东省心理援助热线": "020-81899120",
        "广州市心理援助热线": "020-81899120",
        "青少年法律与心理咨询热线": "12355",
        "全国青少年心理健康专线": "4000-100-525",
        "服务时间": "24小时"
    },
    "江苏": {
        "江苏省心理援助热线": "025-83712977",
        "南京市心理援助中心": "025-83712977",
        "青少年法律与心理咨询热线": "12355",
        "全国青少年心理健康专线": "4000-100-525",
        "服务时间": "24小时"
    },
    "浙江": {
        "浙江省心理援助热线": "0571-85029595",
        "杭州市心理援助热线": "0571-85029595",
        "青少年法律与心理咨询热线": "12355",
        "全国青少年心理健康专线": "4000-100-525",
        "服务时间": "24小时"
    },
    "四川": {
        "四川省心理援助热线": "028-87577510",
        "成都市心理援助热线": "028-87528604",
        "青少年法律与心理咨询热线": "12355",
        "全国青少年心理健康专线": "4000-100-525",
        "服务时间": "24小时"
    },
    "湖北": {
        "湖北省心理援助热线": "027-85844666",
        "武汉市心理医院热线": "027-85844666",
        "青少年法律与心理咨询热线": "12355",
        "全国青少年心理健康专线": "4000-100-525",
        "服务时间": "24小时"
    },
    "陕西": {
        "陕西省心理援助热线": "029-63616911",
        "西安市心理援助热线": "029-63616911",
        "青少年法律与心理咨询热线": "12355",
        "全国青少年心理健康专线": "4000-100-525",
        "服务时间": "24小时"
    },
    "default": {
        "青少年法律与心理咨询热线": "12355",
        "全国青少年心理健康专线": "4000-100-525",
        "全国心理援助热线": "400-161-9995",
        "服务时间": "24小时"
    }
}

# Hugging Face Token - 请替换为您的真实token
# HF_TOKEN = "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"
HF_TOKEN = "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"

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# 情感分类 - 使用更准确的情感分析模型
EMOTION_API_URL = "https://api-inference.huggingface.co/models/bhadresh-savani/bert-base-uncased-emotion"

# 情感强度分析 - 换用更准确的情感强度分析模型
INTENSITY_API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"

# 安抚API - 使用文本生成模型（确保可用的模型）
COMFORT_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

# 安全规则表格 - 根据提供的表格定义
SAFETY_RULES = {
    "高兴": {"low": "normal", "medium": "normal", "high": "normal"},
    "悲伤": {"low": "normal", "medium": "normal", "high": "caution"},
    "愤怒": {"low": "normal", "medium": "caution", "high": "critical"},
    "恐惧": {"low": "normal", "medium": "caution", "high": "critical"},
    "惊讶": {"low": "normal", "medium": "normal", "high": "normal"},
    "厌恶": {"low": "normal", "medium": "caution", "high": "caution"}
}

# 紧急关键词列表 - 需要根据实际情况扩展
CRITICAL_KEYWORDS = [
    "自杀", "自残", "杀人", "伤害", "死了算了", "不想活了", "活够了",
    "跳楼", "跳河", "上吊", "割腕", "安眠药", "同归于尽", "报复社会"
]

# Ekman 6情绪映射表 - 针对新模型优化
EKMAN_MAPPING = {
    # 高兴/快乐
    "joy": "高兴", "happy": "高兴", "happiness": "高兴", "love": "高兴",
    "optimism": "高兴", "excitement": "高兴", "amusement": "高兴",

    # 悲伤
    "sadness": "悲伤", "sad": "悲伤", "grief": "悲伤", "disappointment": "悲伤",
    "remorse": "悲伤", "sorrow": "悲伤",

    # 愤怒
    "anger": "愤怒", "angry": "愤怒", "rage": "愤怒", "fury": "愤怒",
    "annoyance": "愤怒", "irritation": "愤怒",

    # 恐惧
    "fear": "恐惧", "scared": "恐惧", "terror": "恐惧", "anxiety": "恐惧",
    "nervousness": "恐惧", "panic": "恐惧",

    # 惊讶
    "surprise": "惊讶", "surprised": "惊讶", "amazement": "惊讶",
    "astonishment": "惊讶", "shock": "惊讶",

    # 厌恶
    "disgust": "厌恶", "disgusted": "厌恶", "revulsion": "厌恶",
    "contempt": "厌恶", "hatred": "厌恶"
}


def set_current_province(province):
    """设置当前地点"""
    global CURRENT_PROVINCE
    CURRENT_PROVINCE = province
    print(f"📍 当前地点已设置为: {province}")


def get_mental_health_hotlines():
    """根据当前地点返回心理健康热线"""
    global CURRENT_PROVINCE

    # 获取当前地点的热线，如果没有则使用默认
    if CURRENT_PROVINCE in MENTAL_HEALTH_HOTLINES:
        hotlines = MENTAL_HEALTH_HOTLINES[CURRENT_PROVINCE]
    else:
        hotlines = MENTAL_HEALTH_HOTLINES["default"]
        print(f"⚠️  未找到 {CURRENT_PROVINCE} 的热线信息，使用全国默认热线")

    # 确保包含两个必选热线
    required_hotlines = {
        "青少年法律与心理咨询热线": "12355",
        "全国青少年心理健康专线": "4000-100-525"
    }

    # 合并热线，确保必选热线存在
    merged_hotlines = {**hotlines, **required_hotlines}

    return merged_hotlines


def format_hotlines_for_display(hotlines):
    """格式化热线信息用于显示"""
    display_lines = []

    # 先添加两个必选热线
    display_lines.append(f"📞 青少年法律与心理咨询热线: {hotlines['青少年法律与心理咨询热线']}")
    display_lines.append(f"📞 全国青少年心理健康专线: {hotlines['全国青少年心理健康专线']}")

    # 添加其他热线（排除重复和必选的）
    added_count = 2
    for name, number in hotlines.items():
        if name not in ["青少年法律与心理咨询热线", "全国青少年心理健康专线", "服务时间"] and added_count < 5:
            display_lines.append(f"📞 {name}: {number}")
            added_count += 1

    # 添加服务时间
    if "服务时间" in hotlines:
        display_lines.append(f"⏰ 服务时间: {hotlines['服务时间']}")

    return display_lines


def call_huggingface_api(api_url, text):
    """调用Hugging Face API的通用函数，只调用一次"""
    try:
        payload = {"inputs": text}
        print(f"调用API: {api_url.split('/')[-1]}")

        response = requests.post(api_url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            print(f"API调用成功")
            return result
        elif response.status_code == 503:
            print("模型正在加载，无法立即响应")
            return {"error": "model_loading"}
        elif response.status_code == 404:
            print(f"模型不存在或无法访问: {api_url}")
            return {"error": "model_not_found"}
        else:
            print(f"API调用失败: {response.status_code}")
            print(f"错误信息: {response.text[:200]}...")
            return {"error": f"http_error_{response.status_code}"}

    except requests.exceptions.Timeout:
        print(f"API调用超时")
        return {"error": "timeout"}

    except Exception as e:
        print(f"API调用异常: {e}")
        return {"error": f"exception_{str(e)}"}


def extract_keywords(text):
    """提取关键词"""
    # 简单的关键词提取，可以根据需求扩展
    keywords = re.findall(r'[\u4e00-\u9fff]{2,}', text)
    # 去除常见停用词
    stop_words = ['为什么', '大家', '我的', '你的', '这个', '那个', '就是', '可以', '应该']
    keywords = [kw for kw in keywords if kw not in stop_words and len(kw) > 1]

    return keywords[:10]  # 返回前10个关键词









def get_fallback_comfort_message(analysis_data):
    """回退安抚消息"""
    emotion = analysis_data['mark_a']['primary_emotion']
    intensity = analysis_data['mark_b']['intensity']

    comfort_messages = {
        "悲伤": [
            "我能感受到您现在的痛苦，请记住您并不孤单。悲伤是正常的情绪，给自己一些时间和空间。",
            "我理解您的心情，悲伤时需要被理解和陪伴。请相信，艰难的时刻会过去的。",
            "您的感受很重要，悲伤是人之常情。我会在这里陪伴您，支持您度过这个时刻。"
        ],
        "愤怒": [
            "我理解您现在很生气，让我们先深呼吸几次。强烈的情绪需要被看见和理解。",
            "愤怒是正常的情绪反应，我理解您的感受。让我们一起冷静下来，找到更好的解决方法。",
            "我能感受到您的愤怒，这种情绪很强烈。请给自己一点空间，我会在这里支持您。"
        ],
        "恐惧": [
            "害怕是正常的反应，您现在很安全。让我们一起面对这些恐惧。",
            "我理解您的恐惧，这种感觉很真实。请记住，您不是一个人在面对这些。",
            "恐惧来临时确实让人不安，但请相信您有能力应对。我会在这里陪伴您。"
        ],
        "厌恶": [
            "我理解您的反感情绪，有些情况确实让人难以接受。我们可以一起找到更好的应对方式。",
            "厌恶的感觉很不舒服，我理解您的感受。让我们试着从不同角度看待这个问题。",
            "这种反感情绪很正常，重要的是我们如何应对。我会支持您找到解决的方法。"
        ],
        "高兴": [
            "很高兴看到您有积极的情绪！请享受这份美好，同时也要记得照顾好自己的各种情绪。",
            "积极的情绪很宝贵，我为您感到高兴。请继续保持这种状态。",
            "看到您心情不错，这很棒！情绪有起伏是正常的，享受当下的美好时刻。"
        ],
        "惊讶": [
            "意外的情况确实会让人感到惊讶，我理解您的感受。让我们一起理清思路。",
            "惊讶的情绪很自然，面对突发情况时我们都会有这样的反应。",
            "我理解您的惊讶，这种情况确实出乎意料。让我们慢慢处理。"
        ]
    }

    messages = comfort_messages.get(emotion, comfort_messages['高兴'])  # 默认使用高兴
    # 根据强度选择不同的消息
    message_index = min(int(intensity * len(messages)), len(messages) - 1)
    message = messages[message_index]

    return {
        "comfort_message": message,
        "emergency_contact_initiated": True,
        "source": "fallback_comfort"
    }


def ekman_emotion_classification(text):
    """
    情感分类 - 使用更准确的情感分析模型，只调用一次
    """
    print("=== 开始情感分类 ===")

    api_result = call_huggingface_api(EMOTION_API_URL, text)

    if api_result is None or "error" in api_result:
        print("情感分析API调用失败，使用回退方案")
        return get_fallback_emotion(text)

    return process_emotion_result(api_result, text)


def process_emotion_result(api_result, text):
    """处理情感分类结果"""
    try:
        processed_results = []
        primary_emotion = "高兴"  # 默认改为高兴
        max_score = 0

        # 处理API响应格式
        if isinstance(api_result, list) and len(api_result) > 0:
            emotions_data = api_result[0]
        else:
            emotions_data = api_result

        # 确保数据格式正确
        if not isinstance(emotions_data, list):
            print(f"API返回格式异常: {type(emotions_data)}，使用回退方案")
            return get_fallback_emotion(text)

        for item in emotions_data:
            if isinstance(item, dict):
                label = item.get('label', '')
                score = item.get('score', 0)

                # 映射到Ekman情绪
                emotion_label = EKMAN_MAPPING.get(label, None)
                if emotion_label is None:
                    emotion_label = EKMAN_MAPPING.get(label.lower(), None)

                # 如果映射成功，添加到结果中
                if emotion_label:
                    processed_results.append({
                        'original_label': label,
                        'emotion_label': emotion_label,
                        'score': score
                    })

                    # 找到主要情绪
                    if score > max_score:
                        max_score = score
                        primary_emotion = emotion_label

        # 如果没有找到有效情绪，使用回退
        if not processed_results:
            return get_fallback_emotion(text)

        mark_a = {
            'primary_emotion': primary_emotion,
            'confidence': max_score,
            'all_emotions': processed_results
        }

        return mark_a

    except Exception as e:
        print(f"处理情感结果时出错: {e}")
        return get_fallback_emotion(text)


def emotion_intensity_analysis(text):
    """
    情感强度分析 - 使用更准确的情感分析模型
    """
    print("=== 开始情感强度分析 ===")
    api_result = call_huggingface_api(INTENSITY_API_URL, text)

    if api_result is None or "error" in api_result:
        print("强度分析API失败，使用回退方案")
        return get_fallback_intensity(text)

    return process_intensity_result(api_result, text)


def process_intensity_result(api_result, text):
    """处理强度分析结果"""
    try:
        if isinstance(api_result, list) and len(api_result) > 0:
            intensity_data = api_result[0]

            # 新模型返回正面、负面、中性三种情感
            positive_score = 0
            negative_score = 0
            neutral_score = 0

            for item in intensity_data:
                if isinstance(item, dict):
                    label = item.get('label', '')
                    score = item.get('score', 0)

                    if 'positive' in label.lower() or 'pos' in label.lower():
                        positive_score = score
                    elif 'negative' in label.lower() or 'neg' in label.lower():
                        negative_score = score
                    elif 'neutral' in label.lower():
                        neutral_score = score

            # 新的强度计算逻辑：基于情感极性和置信度
            if positive_score > negative_score:
                # 正面情感，强度基于正面分数
                base_intensity = positive_score
            else:
                # 负面情感，强度基于负面分数
                base_intensity = negative_score

            # 确保强度在合理范围内
            intensity = min(max(base_intensity, 0), 1.0)

            # 基于文本特征微调
            adjusted_intensity = adjust_intensity_with_features(intensity, text)

            mark_b = {
                'intensity': adjusted_intensity,
                'level': get_intensity_level(adjusted_intensity),
                'raw_intensity': intensity,
                'positive_score': positive_score,
                'negative_score': negative_score,
                'neutral_score': neutral_score
            }

            return mark_b
        else:
            return get_fallback_intensity(text)
    except Exception as e:
        print(f"处理强度结果时出错: {e}")
        return get_fallback_intensity(text)


def adjust_intensity_with_features(base_intensity, text):
    """基于文本特征调整强度值 - 更保守的调整"""
    adjusted_intensity = base_intensity

    # 1. 感叹号增强（更保守）
    exclamation_count = text.count('!') + text.count('！')
    if exclamation_count > 0:
        adjusted_intensity += min(exclamation_count * 0.05, 0.15)

    # 2. 强度副词增强（更保守）
    intensity_adverbs = ['非常', '很', '特别', '极其', '超级', '十分', '太', '真的', '超级', '极度']
    adverb_count = sum(text.count(adverb) for adverb in intensity_adverbs)
    if adverb_count > 0:
        adjusted_intensity += min(adverb_count * 0.04, 0.12)

    # 3. 重复词增强
    words = re.findall(r'[\u4e00-\u9fff]+', text)
    for word in words:
        if len(word) > 1 and text.count(word) > 1:
            adjusted_intensity += 0.03
            break

    # 4. 情感词增强（更保守）
    emotional_words = ['痛苦', '绝望', '崩溃', '疯狂', '幸福', '快乐', '兴奋', '恐惧']
    emotional_count = sum(text.count(word) for word in emotional_words)
    if emotional_count > 0:
        adjusted_intensity += min(emotional_count * 0.03, 0.1)

    return min(max(adjusted_intensity, 0), 1.0)


def get_fallback_emotion(text):
    """情绪分类回退方案 - 只返回Ekman6种情感"""
    print("使用回退方案进行情感分析")
    emotion_keywords = {
        '高兴': ['开心', '快乐', '高兴', '幸福', '满意', '兴奋', '愉快', '喜悦', '棒', '好', '喜欢', '爱', '哈哈',
                 '呵呵'],
        '悲伤': ['难过', '悲伤', '伤心', '绝望', '痛苦', '郁闷', '沮丧', '悲哀', '哭', '泪', '失望', '难受'],
        '愤怒': ['生气', '愤怒', '气愤', '恼火', '讨厌', '恨', '暴躁', '怨恨', '怒', '烦', '愤怒', '气死'],
        '恐惧': ['害怕', '恐惧', '紧张', '焦虑', '担心', '恐慌', '惊慌', '怕', '吓', '恐惧', '不安'],
        '惊讶': ['惊讶', '惊奇', '吃惊', '意外', '震惊', '哇', '天啊', '没想到', '居然', '竟然'],
        '厌恶': ['厌恶', '恶心', '反感', '嫌弃', '憎恶', '吐', '呕', '讨厌', '烦人', '受不了']
    }

    emotion_scores = {}

    for emotion, keywords in emotion_keywords.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 1
        if score > 0:
            emotion_scores[emotion] = score

    if emotion_scores:
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = min(emotion_scores[primary_emotion] * 0.2, 0.8)
    else:
        # 如果没有匹配到关键词，默认返回高兴（而不是中性）
        primary_emotion = "高兴"
        confidence = 0.3

    return {
        'primary_emotion': primary_emotion,
        'confidence': confidence,
        'all_emotions': [{'original_label': 'fallback', 'emotion_label': primary_emotion, 'score': confidence}]
    }


def get_fallback_intensity(text):
    """强度分析回退方案 - 更保守的强度计算"""
    print("使用回退方案进行强度分析")
    intensity_factors = []

    # 1. 文本长度因素（更保守）
    length_factor = min(len(text) / 100, 1.0)  # 调整为100字符
    intensity_factors.append(length_factor * 0.15)

    # 2. 感叹号数量（更保守）
    exclamation_count = text.count('!') + text.count('！')
    exclamation_factor = min(exclamation_count / 5, 1.0)  # 调整为5个感叹号
    intensity_factors.append(exclamation_factor * 0.2)

    # 3. 强度副词（更保守）
    intensity_adverbs = ['非常', '很', '特别', '极其', '超级', '十分', '太', '真的', '超级']
    adverb_count = sum(text.count(adverb) for adverb in intensity_adverbs)
    adverb_factor = min(adverb_count / 4, 1.0)  # 调整为4个副词
    intensity_factors.append(adverb_factor * 0.3)

    # 4. 情感词强度（更保守）
    strong_emotional_words = ['痛苦', '绝望', '崩溃', '疯狂', '幸福', '快乐', '兴奋', '恐惧']
    strong_word_count = sum(text.count(word) for word in strong_emotional_words)
    strong_word_factor = min(strong_word_count / 3, 1.0)  # 调整为3个情感词
    intensity_factors.append(strong_word_factor * 0.35)

    total_intensity = sum(intensity_factors)

    return {
        'intensity': min(total_intensity, 1.0),
        'level': get_intensity_level(total_intensity),
        'raw_intensity': total_intensity
    }


def get_intensity_level(intensity):
    """根据强度值返回等级"""
    if intensity >= 0.7:
        return "高"
    elif intensity >= 0.4:  # 调整中等阈值
        return "中等"
    else:
        return "低"


def get_intensity_category(intensity):
    """根据强度值返回安全分类（低/中/高）"""
    if intensity >= 0.7:  # 调整阈值
        return "high"
    elif intensity >= 0.4:
        return "medium"
    else:
        return "low"


def check_critical_keywords(text):
    """检查紧急关键词"""
    text_lower = text.lower()
    found_keywords = []

    for keyword in CRITICAL_KEYWORDS:
        if keyword in text_lower:
            found_keywords.append(keyword)

    return found_keywords


def safety_classification(mark_a, mark_b, text):
    """
    安全检查分类
    根据情绪类型和强度，结合关键词进行安全评估
    """
    primary_emotion = mark_a['primary_emotion']
    intensity_value = mark_b['intensity']

    # 获取强度分类
    intensity_category = get_intensity_category(intensity_value)

    # 根据规则表格获取基础安全等级
    base_safety_level = SAFETY_RULES.get(primary_emotion, {}).get(intensity_category, "normal")

    # 检查紧急关键词
    critical_keywords = check_critical_keywords(text)

    # 安全评估逻辑
    safety_result = {
        'base_safety_level': base_safety_level,
        'critical_keywords_found': critical_keywords,
        'final_safety_level': base_safety_level,
        'should_interrupt': False,
        'emergency_contact': False
    }

    # 如果有紧急关键词，升级为critical
    if critical_keywords:
        safety_result['final_safety_level'] = 'critical'

    # 如果是critical级别，设置中断标志
    if safety_result['final_safety_level'] == 'critical':
        safety_result['should_interrupt'] = True
        safety_result['emergency_contact'] = True

    return safety_result


# 接口函数
def analyze_user_text(text):
    """
    主要分析函数 - 完成第1-3层分析
    如果检测到critical情况，立即中断并启动紧急流程
    """
    print(f"\n📝 分析用户输入: {text}")
    print("=" * 60)

    # 1. 情感分类 (标记a)
    mark_a = ekman_emotion_classification(text)
    print(f"🎭 情绪分类结果:")
    print(f"   → 主要情绪: {mark_a['primary_emotion']}")
    print(f"   → 置信度: {mark_a['confidence']:.2f}")

    # 2. 情感强度分析 (标记b)
    mark_b = emotion_intensity_analysis(text)
    print(f"📊 情感强度分析:")
    print(f"   → 强度值: {mark_b['intensity']:.2f}")
    print(f"   → 强度等级: {mark_b['level']}")

    # 3. 关键词提取
    keywords = extract_keywords(text)
    print(f"🔑 关键词提取:")
    print(f"   → 关键词: {keywords}")

    # 4. 安全检查分类
    safety_result = safety_classification(mark_a, mark_b, text)
    print(f"🛡️ 安全检查结果:")
    print(f"   → 基础安全等级: {safety_result['base_safety_level']}")
    print(f"   → 最终安全等级: {safety_result['final_safety_level']}")
    print(f"   → 检测到关键词: {safety_result['critical_keywords_found']}")
    print(f"   → 是否需要中断: {'是' if safety_result['should_interrupt'] else '否'}")
    print(f"   → 是否需要紧急联系: {'是' if safety_result['emergency_contact'] else '否'}")

    # 构建完整分析数据
    analysis_data = {
        "mark_a": mark_a,  # 情感分类
        "mark_b": mark_b,  # 情感强度
        "keywords": keywords,  # 关键词
        "safety_result": safety_result,  # 安全分类
        "user_text": text  # 用户原始文本
    }

    # 5. 如果达到critical级别，触发紧急协议并真正中断
    if safety_result['should_interrupt']:
        print("🚨 检测到紧急情况，启动紧急协议...")

        # 第一步：调用Hugging Face安抚API
        comfort_response = send_to_comfort_api(analysis_data, text)
        print(f"💬 安抚回复: {comfort_response.get('comfort_message', '安抚消息发送成功')}")

        # 第二步：获取并显示心理健康热线
        hotlines = get_mental_health_hotlines()
        hotline_display = format_hotlines_for_display(hotlines)

        print("📞 建议拨打的心理健康热线:")
        for line in hotline_display:
            print(f"   {line}")

        print("💡 请立即拨打以上热线寻求专业帮助！")

        # 返回中断响应，不继续后续处理
        result = {
            "processing_complete": False,
            "emergency_triggered": True,
            "safety_level": "critical",
            "comfort_response": comfort_response,
            "recommended_hotlines": hotlines,
            "hotlines_display": hotline_display,
            "analysis_data": analysis_data,  # 包含分析结果，但标记为已中断
            "message": "检测到紧急情况，已提供安抚回复和心理健康热线建议，后续处理已中断"
        }

        print("❌ 处理已中断，已建议用户拨打心理健康热线")

    else:
        # 正常情况，继续后续处理
        result = {
            "processing_complete": True,
            "emergency_triggered": False,
            "safety_result": safety_result,  # 安全分类
            "mark_a": mark_a,  # 情感分类
            "mark_b": mark_b,  # 情感强度
            "keywords": keywords,  # 关键词
            "message": "第1-3层分析完成，准备进行后续处理"
        }
        print("✅ 第1-3层分析完成")

    print("=" * 60)
    return result


def main():
    """主函数：允许用户输入自己的语句"""
    print("🎭 情感分析系统启动")
    print("=" * 50)

    # 设置地点（在代码中设置）
    set_current_province(CURRENT_PROVINCE)
    print(f"📍 当前地点: {CURRENT_PROVINCE}")

    print("\n💬 请输入您想要分析的语句（输入'退出'或'quit'结束程序）:")
    print("-" * 50)

    while True:
        # 获取用户输入
        user_input = input("\n请输入语句: ").strip()

        # 检查退出条件
        if user_input.lower() in ['退出', 'quit', 'exit']:
            print("感谢使用情感分析系统，再见！")
            break

        # 检查空输入
        if not user_input:
            print("⚠️  输入不能为空，请重新输入。")
            continue

        print("\n" + "=" * 60)
        print("开始分析...")

        try:
            # 调用分析函数
            result = analyze_user_text(user_input)

            # 显示结果摘要
            print("\n📋 分析结果摘要:")
            print(f"   情绪: {result.get('mark_a', {}).get('primary_emotion', '未知')}")
            print(
                f"   强度: {result.get('mark_b', {}).get('intensity', 0):.2f} ({result.get('mark_b', {}).get('level', '未知')})")
            print(f"   安全等级: {result.get('safety_result', {}).get('final_safety_level', '未知')}")

            if result.get('emergency_triggered'):
                print("   🚨 已触发紧急协议，请立即寻求专业帮助！")

        except Exception as e:
            print(f"❌ 分析过程中出现错误: {e}")
            print("请稍后重试或联系技术支持。")

        print("=" * 60)
        print("\n您可以继续输入其他语句进行分析，或输入'退出'结束程序。")
        return result


def api():
    print("\n💬 请输入您想要分析的语句（输入'退出'或'quit'结束程序）:")
    print("-" * 50)
    # 获取用户输入
    user_input = input("\n请输入语句: ").strip()

    # 检查退出条件
    if user_input.lower() in ['退出', 'quit', 'exit']:
        print("感谢使用情感分析系统，再见！")
        return result

    # 检查空输入
    if not user_input:
        print("⚠️  输入不能为空，请重新输入。")
        return result

    print("\n" + "=" * 60)
    print("开始分析...")

    try:
        # 调用分析函数
        result = analyze_user_text(user_input)

        # 显示结果摘要
        print("\n📋 分析结果摘要:")
        print(f"   情绪: {result.get('mark_a', {}).get('primary_emotion', '未知')}")
        print(
            f"   强度: {result.get('mark_b', {}).get('intensity', 0):.2f} ({result.get('mark_b', {}).get('level', '未知')})")
        print(f"   安全等级: {result.get('safety_result', {}).get('final_safety_level', '未知')}")

        if result.get('emergency_triggered'):
            print("   🚨 已触发紧急协议，请立即寻求专业帮助！")

    except Exception as e:
        print(f"❌ 分析过程中出现错误: {e}")
        print("请稍后重试或联系技术支持。")

    print("=" * 60)
    print("\n您可以继续输入其他语句进行分析，或输入'退出'结束程序。")
    return result


# 测试示例
if __name__ == '__main__':
    # 直接运行主函数，让用户输入语句
    main()

