.PHONY: preview build tidy

preview:
	hugo server --disableFastRender

build:
	hugo --gc --minify

tidy:
	hugo mod tidy
