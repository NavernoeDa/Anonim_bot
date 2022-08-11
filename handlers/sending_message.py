def send_message(message, bot, id_user):
    dict_message = {
        message.sticker: lambda id_: bot.send_sticker(id_, message.sticker.file_id),
        message.audio: lambda id_: bot.send_audio(id_, message.audio.file_id),
        message.animation: lambda id_: bot.send_animation(id_, message.animation.file_id),
        message.document: lambda id_: bot.send_document(id_, message.document.file_id),
        message.voice: lambda id_: bot.send_voice(id_, message.voice.file_id),
        message.video_note: lambda id_: bot.send_video_note(id_, message.video_note.file_id),
        message.video: lambda id_: bot.send_video(id_, message.video.file_id),
        message.reply_to_message: lambda id_: bot.send_message(id_, f'Исходное сообщение: {message.reply_to_message.text}'
                                                                    f'\n\nОтвет: {message.text}'),
        message.text: lambda id_: bot.send_message(id_, message.text)
    }

    for key, func in dict_message.items():
        if key:
            return func(id_user)
