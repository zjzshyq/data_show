import bar_chart_race as bcr
video_path = "/Users/huyiqing/Movies/py4v/covid_race.mp4"
df = bcr.load_dataset('covid19')
bcr.bar_chart_race(df, filename=video_path)
print(f"视频已保存到: {video_path}")
