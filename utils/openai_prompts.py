classification_prompt = """
You are given a whatsapp message from a user of our app (with some additional context). We would like you to extract following information from it:
- Potential Name of the User [<Name>, null]
- What the user is asking for: ['Question', 'Weather Data', 'Miscellaneous']
- Is the user asking for data at a specific time: [<Time as ISO 8601>, null]
- What language / dialect is the person speaking: [<Language>, null]
- How good is the users literacy: ['Good', 'Bad', 'Average', null]

## Steps:
1. Read the message carefully.
2. Extract the information mentioned above.
3. If any information is not present, mark it as null.
4. Return the extracted information as a json object.

## Output Format:
We would like you to return the fields as a json object. If a field is not present, do not include it in the json object.
Always include the question field.
```json
{
    "name": "<Name>",
    "question": "<Question/Weather Data/Miscellaneous>",
    "time": "<Time as ISO 8601>",
    "language": "<Language>",
    "literacy": "<Good/Bad/Average>",
}
```

## Example:
Given the message and context:
```text
# Message
Hey, can you tell me what the weather is like tomorrow?

# Context
Date and Time: 2022-02-01 12:00:00
Potential Name: Marcus
```

The extracted information would be:
```json
{
    "name": "Marcus",
    "question": "Weather Data",
    "time": "2022-02-02T00:00:00Z",
    "language": "English",
    "literacy": "Good"
}
```

## Notes:
- If the information is not present, do not include it in the json object.
- The user may not always provide all the information.
- Make sure to format the json correctly.
- The time should be formatted in ISO 8601 format.
- Always include the question field.
"""