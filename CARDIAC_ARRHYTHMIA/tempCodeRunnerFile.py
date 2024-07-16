class UserMainCode(object):
    @classmethod
    def min_window(cls, s, t):
        from collections import defaultdict
        
        
        if not s or not t or len(s) < len(t):
            return ""
        
        # Frequency maps
        freq_t = defaultdict(int)
        freq_window = defaultdict(int)
        
        # Count characters in t
        for char in t:
            freq_t[char] += 1
        
        # Variables to track minimum window
        min_len = float('inf')
        min_window = ""
        required_chars = len(freq_t)
        formed_chars = 0
        left = 0
        
        # Sliding window variables
        for right in range(len(s)):
            # Expand window to the right
            char_right = s[right]
            freq_window[char_right] += 1
            
            # Check if current character is part of the required characters
            if char_right in freq_t and freq_window[char_right] == freq_t[char_right]:
                formed_chars += 1
            
            # Shrink window from the left if all required characters are formed
            while formed_chars == required_chars and left <= right:
                char_left = s[left]
                
                # Update minimum window if smaller
                if (right - left + 1) < min_len:
                    min_len = right - left + 1
                    min_window = s[left:right + 1]
                
                # Remove char_left from window
                freq_window[char_left] -= 1
                if char_left in freq_t and freq_window[char_left] < freq_t[char_left]:
                    formed_chars -= 1
                
                # Move left pointer
                left += 1
        
        return min_window

# Example usage:
s = "ADOBECODEBANC"
t = "ABC"
print(UserMainCode.min_window(s, t))  # Output should be "BANC"