import LLM_1_3_02
import json


class Emotion_strategy:
    safe_level = None
    kewords = None
    emotion = 0
    intensity = 0
    order = 0
    strategy_line = [
        '''回复语气：冷静、坚定、安抚
   回复字数范围：50-100字
   说话技巧：先认可情绪（如“我理解你为什么生气”），再提供解决方案或道歉，避免争论或否定感受。
   核心目的：降低愤怒情绪，防止冲突升级，引导理性对话。
   ''',
        '''回复语气：理解、合作
   回复字数范围：30-70字
   说话技巧：倾听并表达理解（如“这件事确实让人不满”），寻求共同点，提出建设性意见。
   核心目的：化解怒气，促进沟通，解决问题。
   ''',
        '''回复语气：轻松、幽默
   回复字数范围：20-50字
   说话技巧：轻描淡写地回应（如“别让小事影响心情”），转移话题或使用幽默化解。
   核心目的：快速缓解轻微不快，维持轻松氛围。
   ''',
        '''回复语气：安慰、保护
   回复字数范围：60-120字
   说话技巧：提供安全感（如“我会陪你一起面对”），解释情况以减少不确定性，鼓励深呼吸或行动。
   ''',
        '''回复语气：鼓励、支持
    回复字数范围：40-80字
    说话技巧：肯定感受（如“你的担心是正常的”），提供资源或建议，鼓励面对恐惧。
    核心目的：增强信心，减少焦虑，促进积极应对。
    ''',
        '''回复语气：轻松、安心
   回复字数范围：20-60字
   说话技巧：简单安慰（如“没事的，放松点”），正常化情绪，提供 reassurance。
   核心目的：快速消除顾虑，保持平静。
   ''',
        '''回复语气：同情、温暖
   回复字数范围：70-150字
   说话技巧：深度倾听（如“我在这里听你说”），表达共情，分享类似经历，提供陪伴或帮助。
   核心目的：提供情感支持，缓解悲伤，促进宣泄。
   ''',
        '''回复语气：关怀、鼓励
   回复字数范围：50-100字
   说话技巧：认可情绪（如“难过是正常的”），分享积极视角，建议分散注意力的活动。
   核心目的：提升情绪，促进恢复，鼓励向前看。
   ''',
        '''回复语气：温和、乐观
   回复字数范围：30-70字
   说话技巧：简短安慰（如“一切都会好起来的”），正面引导，强调希望。
   核心目的：轻推向积极方向，防止情绪恶化。
   ''',
        '''回复语气：兴奋、分享
   回复字数范围：40-90字
   说话技巧：共同庆祝（如“太为你高兴了！”），放大快乐，肯定成就，询问细节。
   核心目的：强化积极情绪，加强关系，分享快乐。
   ''',
        '''回复语气：愉快、认可
   回复字数范围：30-70字
   说话技巧：表达高兴（如“这真是个好消息”），鼓励继续努力，分享类似喜悦。
   核心目的：支持快乐，维持积极状态，增强动力。
   ''',
        '''回复语气：轻松、认可
   回复字数范围：20-50字
   说话技巧：简单称赞（如“真好！”），微笑回应，轻描淡写地认可。
   核心目的：认可小喜悦，保持积极互动。
   ''',
        '''回复语气：中立、客观
   回复字数范围：50-100字
   说话技巧：不强化厌恶（如“我明白你的感受，但让我们看看其他角度”），提供替代视角，分散注意力。
   核心目的：减少厌恶感，避免负面扩散，引导理性思考。
   ''',
        '''回复语气：理解、引导
   回复字数范围：40-80字
   说话技巧：认可感受（如“这确实让人不舒服”），建议忽略或改变焦点，提供中性信息。
   核心目的：化解厌恶，转向中性或积极话题。
   ''',
        '''回复语气：轻松、忽略
   回复字数范围：20-60字
   说话技巧：最小化反应（如“别太在意”），转移话题，使用幽默淡化。
   核心目的：快速跳过厌恶，维持轻松对话。
   ''',
        '''回复语气：震惊、支持
   回复字数范围：50-100字
   说话技巧：分享惊讶（如“我也没想到！”），帮助处理信息，提供冷静建议，鼓励深呼吸。
   核心目的：帮助消化震惊，稳定情绪，促进适应。
   ''',
        '''回复语气：好奇、分享
   回复字数范围：40-80字
   说话技巧：表达兴趣（如“这真有趣，怎么回事？”），探讨原因，共同理解事件。
   核心目的：分享惊讶，增强连接，满足好奇心。
   ''',
        '''回复语气：轻松、有趣
   回复字数范围：20-60字
   说话技巧：简短回应（如“哇，意外！”），幽默处理，轻描淡写。
   核心目的：轻松对待小惊讶，保持对话趣味性。
   ''',
        '''回复语气：极度冷静、稳定、接纳
    回复字数范围：60-120字
    说话技巧：承认情绪的合理性（如“在如此大的压力下，感到愤怒是完全正常的”），将情绪与人分开（“我听到的是你对这件事的强烈感受，而不是你这个人不好”），关注情绪背后的伤痛（“这种愤怒是否也让你感到很受伤？”）。
    ''',
        '''回复语气：理解、探寻
   回复字数范围：40-90字
   说话技巧：验证感受（如“这件事确实让人感到不公平和气愤”），邀请用户分享更多（“你愿意多谈谈是什么让你最生气吗？”），帮助其梳理思绪。
   核心目的：将愤怒转化为可讨论的议题，帮助用户理解自己情绪的来源。
   ''',
        '''回复语气：温和、关注
   回复字数范围：30-70字
   说话技巧：注意到细微变化（如“我感觉到你似乎对这件事有些烦燥”），给予表达空间（“任何细微的感受都值得被在意”）。
   核心目的：捕捉早期情绪信号，防止情绪积累和升级。
   ''',
        '''回复语气：安抚、 grounding（帮助锚定现实）
   回复字数范围：70-150字
   说话技巧：提供安全感（如“现在这个时刻，你是安全的，我在这里陪着你”），使用简单的问题帮助其回到当下（“你能感觉到脚踩在地面上的感觉吗？能告诉我你看到了周围的哪三样东西？”），鼓励寻求专业支持。
   核心目的：在恐慌发作时提供即时稳定感，防止情况恶化，并引导至专业干预。
   ''',
        '''回复语气：鼓励、支持
   回复字数范围：50-100字
   说话技巧：正常化感受（如“面对不确定性，很多人都会感到害怕，这不是你的错”），探讨应对资源（“过去当你感到害怕时，做什么会让自己感觉好一点点？”）。
   核心目的：增强用户的自我效能感，帮助其连接内在和外在的支持资源。
   ''',
        '''回复语气：安心、确认
   回复字数范围：30-80字
   说话技巧：表达共情（如“这种隐隐的担忧确实会消耗人的精力”），温和地挑战灾难化思维（“我们一起来看一下，最坏的情况发生的可能性有多大？”）。
   核心目的：缓解焦虑，引入认知行为疗法（CBT）的简单概念，帮助用户审视想法。
   ''',
        '''回复语气：深沉共情、无条件接纳
   回复字数范围：80-180字
   说话技巧：安静地陪伴（如“我在这里，我听到了你的痛苦”），避免空洞安慰（不要说“想开点”），允许沉默和哭泣（“不需要强忍，哭出来也没关系”）。关键点：评估自伤自杀风险，并直接、关怀地询问（“在你感到如此绝望的时候，有没有想过伤害自己？”）。
   核心目的：提供情感容器，承载极度的悲伤，并进行必要的风险筛查和安全引导。
   ''',
        '''回复语气：温暖、陪伴
   回复字数范围：60-120字
   说话技巧：反映情感（如“失去/经历这些，让你感到心都被掏空了”），连接支持系统（“在你感到悲伤的时候，有可以信赖的人说说话吗？”）。
   核心目的：帮助用户不孤独地面对悲伤，鼓励其建立和利用支持网络。
   ''',
        '''回复语气：温和、关注
   回复字数范围：40-90字
   说话技巧：认可情绪的存在（如“这种淡淡的忧伤也是真实且重要的”），鼓励自我关怀（“今天可以做一件小事来照顾自己吗？比如喝杯热茶”）。
   核心目的：防止情绪沉溺，温和地引导向自我照顾。
   ''',
        '''回复语气：真诚分享、积极关注
   回复字数范围：50-100字
   说话技巧：共同庆祝（如“真为你感到高兴！看到你脸上有笑容太好了”），帮助用户记录这个积极时刻（“这个快乐的瞬间对你来说意味着什么？”）。
   核心目的：放大积极情绪，将其作为对抗心理困境的资源和支持治疗的动力。
   ''',
        '''回复语气：愉快、肯定
   回复字数范围：40-90字
   说话技巧：肯定用户的感受和能力（如“这是你应得的快乐，你为此努力了”），连接积极体验与健康（“注意到没有，当你感到开心时，身体的感受也会轻松一些”）。
   核心目的：强化积极体验，将其正常化，作为康复的一部分。
   ''',
        '''回复语气：温和、留意
   回复字数范围：30-70字
   说话技巧：注意到微光（如“很高兴能看到你有一丝轻松的感觉”），不加压力地认可（“即使是很短暂的平静，也值得珍惜”）。
   核心目的：捕捉并珍惜任何积极的瞬间，不因其微弱而忽视。
   
   ''',
        '''回复语气：中立、探寻根源
   回复字数范围：60-120字
   说话技巧：探索厌恶的对象（如“这种强烈的厌恶感，主要是针对某个具体行为，还是更广泛的感觉？”），可能与创伤有关，需特别谨慎。避免认同其厌恶，而是关注感受本身。
   核心目的：理解厌恶情绪的心理根源，而非处理表面对象。引导至咨询师处进行深度探讨。
   ''',
        '''回复语气：理解、梳理
   回复字数范围：40-90字
   说话技巧：验证感受（如“反复接触让你反感的事物，确实会让人身心俱疲”），帮助设定界限（“这是否提醒你需要和某些人或事保持一点距离？”）。
   核心目的：将厌恶情绪转化为设定健康人际边界或自我保护的信号。
   ''',
        '''回复语气：轻松、探索
   回复字数范围：30-70字
   说话技巧：温和地探讨（如“这种不太舒服的感觉，有没有让你联想到什么？”），不强化也不否定。
   核心目的：作为了解用户偏好和价值观的窗口。
   ''',
        '''回复语气：稳定、帮助整合
   回复字数范围：60-120字
   说话技巧：帮助处理信息（如“这个消息太突然了，你需要一点时间来消化它”），提供稳定的陪伴（“我在这里，你可以慢慢理清思绪，无论你想说什么或不想说什么都可以”）。
   核心目的：在震惊中提供稳定锚点，帮助用户整合信息，防止因冲击而崩溃。
   ''',
        '''回复语气：好奇、陪伴探索
   回复字数范围：40-90字
   说话技巧：共同面对（如“这确实是个意外的消息，我们一起看看这意味着什么”），帮助梳理可能的影响和应对方式。
   核心目的：将惊讶转化为一个可以共同面对和处理的“事件”。
   ''',
        '''回复语气：温和、开放
   回复字数范围：30-70字
   说话技巧：分享观察（如“这个小意外似乎让你有些触动”），邀请分享（“你愿意多聊聊你的想法吗？”）。
   核心目的：保持沟通的开放性，鼓励情绪表达。
   '''

    ]

    def analyze(self):
        '''
            调用first_to_third模块中的api函数进行情感分析，并将结果存储到类属性中。
        '''

        result = LLM_1_3_02.api()
        self.kewords = result['keywords']
        self.safe_level = result['safety_result']['final_safety_level']
        if (result['mark_a']['primary_emotion'] == '愤怒'):
            self.emotion = 1
        elif (result['mark_a']['primary_emotion'] == '恐惧'):
            self.emotion = 2
        elif (result['mark_a']['primary_emotion'] == '悲伤'):
            self.emotion = 3
        elif (result['mark_a']['primary_emotion'] == '高兴'):
            self.emotion = 'mark_b'
        elif (result['mark_a']['primary_emotion'] == '厌恶'):
            self.emotion = 5
        elif (result['mark_a']['primary_emotion'] == '惊讶'):
            self.emotion = 6
        else:
            print('情绪识别失败')
        if (result['mark_b']['level'] == '高'):
            self.intensity = 3
        elif (result['mark_b']['level'] == '中'):
            self.intensity = 2
        elif (result['mark_b']['level'] == '低'):
            self.intensity = 1
        else:
            print('情感强度识别失败')

    def strategy(self):
        '''
             以下是根据六种情绪（生气、恐惧、悲伤、喜悦、厌恶、惊讶）和三种情感强度（高、中、弱）生成的18种情况分析。

        '''
        order = 0
        if self.safe_level == "normal":
            if self.emotion == 1 and self.intensity == 3:
                order = 1
            elif self.emotion == 1 and self.intensity == 2:
                order = 2
            elif self.emotion == 1 and self.intensity == 1:
                order = 3
            elif self.emotion == 2 and self.intensity == 3:
                order = 4
            elif self.emotion == 2 and self.intensity == 2:
                order = 5
            elif self.emotion == 2 and self.intensity == 1:
                order = 6
            elif self.emotion == 3 and self.intensity == 3:
                order = 7
            elif self.emotion == 3 and self.intensity == 2:
                order = 8
            elif self.emotion == 3 and self.intensity == 1:
                order = 9
            elif self.emotion == 4 and self.intensity == 3:
                order = 10
            elif self.emotion == 4 and self.intensity == 2:
                order = 11
            elif self.emotion == 4 and self.intensity == 1:
                order = 12
            elif self.emotion == 5 and self.intensity == 3:
                order = 13
            elif self.emotion == 5 and self.intensity == 2:
                order = 14
            elif self.emotion == 5 and self.intensity == 1:
                order = 15
            elif self.emotion == 6 and self.intensity == 3:
                order = 16
            elif self.emotion == 6 and self.intensity == 2:
                order = 17
            elif self.emotion == 6 and self.intensity == 1:
                order = 18
            else:
                print('情绪或者情绪强度输入错误')
        elif self.safe_level == "caution":
            if self.emotion == 1 and self.intensity == 3:
                order = 19
            elif self.emotion == 1 and self.intensity == 2:
                order = 20
            elif self.emotion == 1 and self.intensity == 1:
                order = 21
            elif self.emotion == 2 and self.intensity == 3:
                order = 22
            elif self.emotion == 2 and self.intensity == 2:
                order = 23
            elif self.emotion == 2 and self.intensity == 1:
                order = 24
            elif self.emotion == 3 and self.intensity == 3:
                order = 25
            elif self.emotion == 3 and self.intensity == 2:
                order = 26
            elif self.emotion == 3 and self.intensity == 1:
                order = 27
            elif self.emotion == 4 and self.intensity == 3:
                order = 28
            elif self.emotion == 4 and self.intensity == 2:
                order = 29
            elif self.emotion == 4 and self.intensity == 1:
                order = 30
            elif self.emotion == 5 and self.intensity == 3:
                order = 31
            elif self.emotion == 5 and self.intensity == 2:
                order = 32
            elif self.emotion == 5 and self.intensity == 1:
                order = 33
            elif self.emotion == 6 and self.intensity == 3:
                order = 34
            elif self.emotion == 6 and self.intensity == 2:
                order = 35
            elif self.emotion == 6 and self.intensity == 1:
                order = 36
            else:
                print('情绪或者情绪强度输入错误')

        elif self.safe_level == "critical":
            return "Unsafe"
        else:
            print('安全等级输入错误')
        self.order = order

    def strategy_word(self):
        return self.strategy_line[self.order - 1]


def main():
    while True:
        emotion_strategy = Emotion_strategy()
        emotion_strategy.analyze()
        emotion_strategy.strategy()
        print("情绪识别结果：", emotion_strategy.emotion)
        print("情感强度识别结果：", emotion_strategy.intensity)
        print("安全等级识别结果：", emotion_strategy.safe_level)
        print("策略识别结果：", emotion_strategy.strategy_word())


def api():
    emotion_strategy = Emotion_strategy()
    emotion_strategy.analyze()
    emotion_strategy.strategy()
    result = json.dumps({"emotion": emotion_strategy.emotion,
                         "intensity": emotion_strategy.intensity,
                         "safe_level": emotion_strategy.safe_level,
                         "strategy_word": emotion_strategy.strategy_word(),
                         "keywords": emotion_strategy.kewords
                         })
    print(result)
    return result


if __name__ == "__main__":
    api()