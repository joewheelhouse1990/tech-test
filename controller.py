import logging
import numpy as np
import functions.musicbrainz_funcs as mbf
import functions.api_lyrics_funcs as alf


# global variables #
# format for log
_LOG_FMT = "%(asctime)s %(levelname)s:%(name)s: %(message)s"


def setup_log():
    logging.basicConfig(
        format=_LOG_FMT,
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    return logger


def handle_count_of_words(wrd_cnts):

    arr = np.array(wrd_cnts)
    arr = np.delete(arr, np.argwhere(arr == None))
    print(arr)
    lyrics = np.sum(arr)
    songs = len(arr)

    print(f"total number of lyrics: {lyrics}")
    print(f"total number of songs found: {songs}")
    print(f"average number of lyrics in song: {lyrics/songs}")
    print(f"average number of whole words: {lyrics//songs}")


def run_job(artist):

    _logger = setup_log()

    _id = mbf.fetch_artist_id(artist)

    if _id is not None:
        _rec_count = mbf.fetch_recording_count(_id)
        _rec_arr = mbf.fetch_recording_list_module(_id, _rec_count)

        word_counts = alf.run_fetch_from_api_lyrics(artist, _rec_arr, _logger)

        handle_count_of_words(word_counts)


if __name__ == '__main__':

    run_job("Coldplay")



# [208 208 208 208 208 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  126 159 146 163 163 163 163 1 184 203 189 356 356 356 356 356 155 153 153
#  153 155 153 153 153 153 153 155 153 153 153 153 153 153 153 124 186 183
#  237 286 286 286 286 286 286 286 286 286 286 286 286 286 286 237 286 286
#  286 286 286 286 138 122 90 90 90 90 90 155 155 206 213 153 153 153 129
#  561 105 105 114 211 211 211 211 206 217 217 161 169 165 0 0 0 138 157 195
#  158 158 158 158 158 158 158 158 158 58 217 126 167 0 172 167 167 167 167
#  167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 172 172
#  167 167 167 167 172 167 167 167 167 172 167 167 167 167 167 167 167 167
#  172 167 167 167 167 167 8 8 238 125 142 114 114 165 103 109 115 115 112
#  115 115 115 115 115 115 115 115 115 112 115 115 115 83 84 84 136 230 230
#  225 230 230 230 230 239 239 224 224 224 224 239 224 239 224 239 224 224
#  224 140 216 216 1 176 176 176 176 176 176 176 176 176 176 176 105 105 319
#  304 217 188 0 0 230 242 230 230 230 230 206 180 174 151 167 146 166 108
#  108 108 93 135 131 176 99 99 99 200 200 200 200 234 137 137 271 271 288
#  288 288 288 271 288 271 271 271 288 288 175 175 59 203 368 175 175 175
#  175 175 168 168 175 168 175 213 154 156 44 44 44 200 209 164 1 1 1 143
#  143 0 143 143 70 70 70 77 77 177 177 164 247 144 165 1 143 143 144 144
#  185 185 0 118 224 1 274 263 263 263 263 263 200 203 0 95 96 96 96 96 96
#  96 96 96 96 96 96 117 117 181 188 152 91 1 216 216 216 216 103 120 116 14
#  92 92 92 194 96 138 189 189 247 247 33 182 182 182 182 182 182 182 182
#  182 182 182 182 182 182 182 182 182 182 182 182 182 182 155 155 155 148 1
#  137 0 211 0 0 0 0 0 0 0 0 107 141 189 0 192 154 153 153 153 308 308 308
#  308 308 308 124 0 287 0 0 0 0 287 0 0 0 287 287 287 287 0 287 287 0 287
#  143 123 108 309 309 316 316 309 309 309 316 316 309 309 218 218 226 218
#  226 222 222 218 218 167 167 167 205 205 205 1 283 283 283 219 219 219 219
#  219 219 219 219 219 219 219 217 219 219 219 219 28 106 166 166 166 166
#  188 180 188 180 180 180 180 180 188 180 180 188 188 263 162 163 162 207
#  207 200 162 161 161 161 161 161 161 161 161 161 161 161 161 132 137 136
#  136 141 79 98 98 98 148 475 475 475 475 189 189 176 180 180 180 282 292
#  282 292 282 282 282 292 282 282 282 282 292 282 292 186 186 163 155 191
#  191 217 217 217 217 0 0 184 184 80 269 269 269 269 158 145 361 145 198
#  204 201 201 201 201 201 201 201 201 201 201 201 201 201 201 201 187 156
#  95 95 95 109]