require 'sinatra'
require 'securerandom'
require 'fileutils'

set :environment, :production

before do
  if Dir.exists?("workdir")
    du = `du -s workdir`.split[0].to_i
    if du * 512 >= 1024 * 1024 * 10
      FileUtils.rm_rf("workdir")
      Dir.mkdir("workdir")
    end
  else
    Dir.mkdir("workdir")
  end
end

get '/' do
  erb :index
end

get '/upload' do
  erb :index
end

post '/upload' do
  if params[:file]
    begin
      name = SecureRandom.hex(16)
      filename = File.join("workdir" , name + ".zip")
      FileUtils.copy(params[:file][:tempfile].to_path, filename)
      files = `zipinfo -1 #{filename}`
      raise "ERROR" if files.lines.grep(/^word\/media\//).empty?
      redirect to('/images/' + name)
    rescue
      File.delete(filename)
      @err = "FAILED to upload a file"
      erb :index
    end
  else
    @err = 'FAILED to upload a file'
    erb :index
  end
end

get '/images/:name' do |name|
  zipfile = File.join("workdir", name + ".zip")
  if name !~ /^[a-f0-9]{32}$/ || !File.exists?(zipfile)
    @err = "Not Found"
    erb :index
  else
    @name = name
    @images = `zipinfo -1 #{zipfile}`.lines.grep(/^word\/media\/[A-Za-z0-9_]+\.[A-Za-z0-9_]+/).map do |path|
      path.delete_prefix("word/media/")
    end
    erb :images
  end
end

get '/image/:name/:image' do
  if params[:name] !~ /^[a-f0-9]{32}$/ || params[:image] !~ /^[A-Za-z0-9_]+\.[A-Za-z0-9_]+$/
    @err = "Not Found"
    erb :index
  else
    zipfile = File.join("workdir", params[:name] + ".zip")
    filedir = File.join("workdir", SecureRandom.hex(16))
    file = File.join(filedir, params[:image])
    system("unzip -j #{zipfile} word/media/#{params[:image]} -d #{filedir}")
    if File.exists?(file)
      send_file(file)
    else
      @err = "Not Found"
      erb :index
    end
  end
end
