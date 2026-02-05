def keyword_segmentation(user_query, dictionary):
    dictionary = set(dictionary)
    memo = {}

    def backtrack(s):
        if s in memo:
            return memo[s]
        if s == "":
            return [""]

        result = []
        for word in dictionary:
            if s.startswith(word):
                remaining = s[len(word):]
                sub_results = backtrack(remaining)
                for sub in sub_results:
                    if sub:
                        result.append(word + " " + sub)
                    else:
                        result.append(word)
        memo[s] = result
        return result

    return backtrack(user_query)

user_query = "everesthikingtrail"
marketing_keywords_dictionary = ["everest", "hiking", "trek"]

print(keyword_segmentation(user_query, marketing_keywords_dictionary))
