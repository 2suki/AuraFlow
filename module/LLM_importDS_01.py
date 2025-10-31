import requests
import json


class DeepSeekResponder:
    def __init__(self, api_key):
        self.api_key = "sk-a3bab9807c604b879f7987b80523cb7e"
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    def generate_response(self, user_message, analysis_result):
        """
        根据情感分析结果生成回复
        """
        # 解析分析结果
        emotion = analysis_result['emotion']
        intensity = analysis_result['intensity']
        safe_level = analysis_result['safe_level']
        strategy_word = analysis_result['strategy_word']
        keywords = analysis_result['keywords']

        # 情感映射
        emotion_map = {1: "愤怒", 2: "恐惧", 3: "悲伤", 4: "高兴", 5: "厌恶", 6: "惊讶"}
        intensity_map = {1: "低", 2: "中", 3: "高"}

        prompt = f"""你是一个情感支持助手。请根据以下分析结果回复用户：

情感分析结果：
- 主要情绪：{emotion_map.get(emotion, '未知')}
- 情感强度：{intensity_map.get(intensity, '未知')}  
- 安全等级：{safe_level}
- 相关关键词：{', '.join(keywords)}

回复策略：
{strategy_word}

请基于以上分析，对用户的这句话进行自然、真诚的回复：

用户说：{user_message}"""

        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.7
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=data, timeout=30)
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"抱歉，我暂时无法回复：{str(e)}"


def main():
    # 初始化DeepSeek
    chat_bot = DeepSeekResponder("sk-a3bab9807c604b879f7987b80523cb7e")

    print("=== 情感支持对话系统 ===")
    print("输入您想说的话，我会根据情感分析结果回复您")
    print("输入 '退出' 结束对话\n")

    while True:
        # 用户输入
        user_input = input("您: ").strip()

        if user_input.lower() in ['退出', 'quit', 'exit']:
            print("再见！")
            break

        if not user_input:
            print("请输入有效内容")
            continue

        try:
            # 第一步：调用第一个代码 LLM_NEW 进行情感分析
            import LLM_1_3_02
            emotion_analysis = LLM_1_3_02.analyze_user_text(user_input)

            # 第二步：调用第二个代码 LLM_4_5 生成回复策略
            import LLM_4_5

            # 创建情感策略实例
            strategy_analyzer = LLM_4_5.Emotion_strategy()

            # 将第一个代码的分析结果映射到第二个代码需要的格式
            # 情感类型映射
            emotion_mapping = {
                '愤怒': 1, '恐惧': 2, '悲伤': 3,
                '高兴': 4, '厌恶': 5, '惊讶': 6
            }

            # 强度等级映射
            intensity_mapping = {'低': 1, '中': 2, '高': 3}

            # 设置分析结果
            strategy_analyzer.emotion = emotion_mapping.get(
                emotion_analysis['mark_a']['primary_emotion'], 4
            )
            strategy_analyzer.intensity = intensity_mapping.get(
                emotion_analysis['mark_b']['level'], 2
            )
            strategy_analyzer.safe_level = emotion_analysis['safety_result']['final_safety_level']
            strategy_analyzer.kewords = emotion_analysis['keywords']

            # 生成策略
            strategy_analyzer.strategy()

            # 构建最终分析结果
            analysis_result = {
                "emotion": strategy_analyzer.emotion,
                "intensity": strategy_analyzer.intensity,
                "safe_level": strategy_analyzer.safe_level,
                "strategy_word": strategy_analyzer.strategy_word(),
                "keywords": strategy_analyzer.kewords
            }

            print(
                f"分析完成: 情绪{analysis_result['emotion']}, 强度{analysis_result['intensity']}, 安全{analysis_result['safe_level']}")

        except Exception as e:
            print(f"分析过程中出错: {e}")
            continue

        # 生成回复
        print("思考中...")
        response = chat_bot.generate_response(
            user_message=user_input,
            analysis_result=analysis_result
        )

        print(f"助手: {response}\n")
def api(user_input):
        chat_bot = DeepSeekResponder("sk-a3bab9807c604b879f7987b80523cb7e")

    
        try:
            # 第一步：调用第一个代码 LLM_NEW 进行情感分析
            import LLM_1_3_02
            emotion_analysis = LLM_1_3_02.analyze_user_text(user_input)

            # 第二步：调用第二个代码 LLM_4_5 生成回复策略
            import LLM_4_5

            # 创建情感策略实例
            strategy_analyzer = LLM_4_5.Emotion_strategy()

            # 将第一个代码的分析结果映射到第二个代码需要的格式
            # 情感类型映射
            emotion_mapping = {
                '愤怒': 1, '恐惧': 2, '悲伤': 3,
                '高兴': 4, '厌恶': 5, '惊讶': 6
            }

            # 强度等级映射
            intensity_mapping = {'低': 1, '中': 2, '高': 3}

            # 设置分析结果
            strategy_analyzer.emotion = emotion_mapping.get(
                emotion_analysis['mark_a']['primary_emotion'], 4
            )
            strategy_analyzer.intensity = intensity_mapping.get(
                emotion_analysis['mark_b']['level'], 2
            )
            strategy_analyzer.safe_level = emotion_analysis['safety_result']['final_safety_level']
            strategy_analyzer.kewords = emotion_analysis['keywords']

            # 生成策略
            strategy_analyzer.strategy()

            # 构建最终分析结果
            analysis_result = {
                "emotion": strategy_analyzer.emotion,
                "intensity": strategy_analyzer.intensity,
                "safe_level": strategy_analyzer.safe_level,
                "strategy_word": strategy_analyzer.strategy_word(),
                "keywords": strategy_analyzer.kewords
            }

            print(
                f"分析完成: 情绪{analysis_result['emotion']}, 强度{analysis_result['intensity']}, 安全{analysis_result['safe_level']}")

        except Exception as e:
            print(f"分析过程中出错: {e}")
            

        # 生成回复
        
        response = chat_bot.generate_response(
            user_message=user_input,
            analysis_result=analysis_result
        )
        result=[response,analysis_result]
        result=json.dumps(result)
        return result

if __name__ == "__main__":
 main()