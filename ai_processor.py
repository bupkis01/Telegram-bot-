import google.generativeai as genai      
import os      

genai.configure(api_key=os.getenv("GOOGLE_AI_KEY"))      

def generate_ai_summary(match):      
    try:      
        model = genai.GenerativeModel("gemini-1.5-pro")      

        prompt = f"""      
        Generate a short, engaging football match summary.      
        Match: {match['home']} vs {match['away']}      
        Score: {match.get('home_score', 'N/A')} - {match.get('away_score', 'N/A')}      
        Status: {match['status']}      
        """      

        response = model.generate_content(prompt)      
        return response.text.strip()      

    except Exception as e:      
        print(f"❌ AI Processing Error: {e}")      
        return "⚠️ Error generating AI match summary..."