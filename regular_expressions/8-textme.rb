#!/usr/bin/env ruby
line = ARGV[0]
if m = line.match(/\[from:(.*?)\].*\[to:(.*?)\].*\[flags:(.*?)\]/)
  puts "#{m[1]},#{m[2]},#{m[3]}"
end
