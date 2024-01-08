# -*-coding:utf-8-*-

import sys
import os

import youtube_dl

import logging
import hashlib

import table

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def set_ydl_opts(id):
    ydl_opts = {
        'format': 'best[ext=flv]/best',
        'outtmpl': f"../../../video/bilibili/{id}.flv",
        'proxy': 'socks5://127.0.0.1:10808',  # 这一行的代理需要自己进行设定
    }
    return ydl_opts


def downloader(url='', movie=None):

    if url == '' and movie == None:
        return None

    if movie == None and url != '':
        with table.get_session() as s:
            movie = s.query(table.Movie).filter_by(url=url).first()
            if movie == None:
                logger.info(f"url = {url}不在数据库中...")
                try:
                    ydl_opts = set_ydl_opts('temp')
                    if os.path.exists(ydl_opts['outtmpl']):
                        os.remove(ydl_opts['outtmpl'])

                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download(url.split(' '))

                    sha256 = hashlib.sha256(
                        open(ydl_opts['outtmpl'], 'rb').read()).hexdigest()
                    logger.info(
                        f"url = {url}的视频已经下载到了{ydl_opts['outtmpl']}\n**请及时重命名或者移走，否则将会被覆盖...\nsha256 = {sha256}\n本视频不会被记录到数据库...")
                except:
                    logger.error(f"下载url = {url}的视频失败...")
                    return False

                return True
    else:
        if movie.download == False:

            ydl_opts = set_ydl_opts(movie.id)
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(movie.url.split(' '))
            except:
                return False
            fn = ydl_opts["outtmpl"][:-3]+'mp4'
            os.system(f'ffmpeg -i {ydl_opts["outtmpl"]} -vcodec copy -acodec copy {fn}')
            os.remove(ydl_opts['outtmpl'])
            movie.sha256 = hashlib.sha256(
                open(fn, 'rb').read()).hexdigest()
            movie.download = 1
            movie.video_path = fn[fn.index(
                "video"):]

            logger.info(
                f'url = {movie.url}的视频已经下载到了{movie.video_path}...\nsha256 = {movie.sha256}')

        else:
            logger.info(
                f'url = {movie.url}的视频已经下载到了{movie.video_path}...\nsha256 = {movie.sha256}')

        return True


def main():

    while True:
        with table.get_session() as s:
            movie = s.query(table.Movie).filter_by(download=0).first()
            if movie == None:  # 数据库中不再存在可以下载的视频了
                break

            logger.info(
                "\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            logger.info(f"开始下载url为{movie.url}的视频")
            tag = downloader(movie=movie)
            if tag == False:
                logger.error(f"url = {movie.url}的视频下载失败...")
            elif tag == None:
                logger.warning(f"传入的参数有误...")
            else:
                s.commit()  # 下载完毕就提交。


if __name__ == '__main__':
    main()
