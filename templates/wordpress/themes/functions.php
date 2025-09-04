<?php
/**
 * {{PROJECT_NAME}} Theme Functions
 * 
 * @package {{PROJECT_NAME}}
 * @version 1.0.0
 * @author Your Name
 * @created {{DATE}}
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Theme setup and initialization
 */
class {{PROJECT_NAME}}_Theme {
    
    public function __construct() {
        add_action('init', array($this, 'init'));
        add_action('after_setup_theme', array($this, 'theme_setup'));
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_action('widgets_init', array($this, 'register_sidebars'));
        add_action('customize_register', array($this, 'customize_register'));
    }
    
    /**
     * Initialize theme
     */
    public function init() {
        // Add custom post types, taxonomies, etc.
        $this->register_custom_post_types();
        $this->register_custom_taxonomies();
    }
    
    /**
     * Theme setup
     */
    public function theme_setup() {
        // Add theme support
        add_theme_support('post-thumbnails');
        add_theme_support('custom-logo');
        add_theme_support('title-tag');
        add_theme_support('custom-header');
        add_theme_support('custom-background');
        add_theme_support('html5', array(
            'search-form',
            'comment-form',
            'comment-list',
            'gallery',
            'caption',
        ));
        
        // Add custom image sizes
        add_image_size('hero-image', 1200, 600, true);
        add_image_size('card-image', 400, 300, true);
        add_image_size('thumbnail-small', 150, 150, true);
        
        // Register navigation menus
        register_nav_menus(array(
            'primary' => esc_html__('Primary Menu', '{{PROJECT_NAME}}'),
            'footer' => esc_html__('Footer Menu', '{{PROJECT_NAME}}'),
        ));
        
        // Load theme textdomain
        load_theme_textdomain('{{PROJECT_NAME}}', get_template_directory() . '/languages');
    }
    
    /**
     * Enqueue scripts and styles
     */
    public function enqueue_scripts() {
        // Theme styles
        wp_enqueue_style(
            '{{PROJECT_NAME}}-style',
            get_stylesheet_uri(),
            array(),
            '1.0.0'
        );
        
        // Custom styles
        wp_enqueue_style(
            '{{PROJECT_NAME}}-custom',
            get_template_directory_uri() . '/assets/css/custom.css',
            array('{{PROJECT_NAME}}-style'),
            '1.0.0'
        );
        
        // Theme scripts
        wp_enqueue_script(
            '{{PROJECT_NAME}}-main',
            get_template_directory_uri() . '/assets/js/main.js',
            array('jquery'),
            '1.0.0',
            true
        );
        
        // Localize script
        wp_localize_script('{{PROJECT_NAME}}-main', 'themeAjax', array(
            'ajaxurl' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('{{PROJECT_NAME}}_nonce'),
        ));
        
        // Comment reply script
        if (is_singular() && comments_open() && get_option('thread_comments')) {
            wp_enqueue_script('comment-reply');
        }
    }
    
    /**
     * Register sidebars
     */
    public function register_sidebars() {
        register_sidebar(array(
            'name' => esc_html__('Primary Sidebar', '{{PROJECT_NAME}}'),
            'id' => 'sidebar-primary',
            'description' => esc_html__('Add widgets here to appear in your primary sidebar.', '{{PROJECT_NAME}}'),
            'before_widget' => '<section id="%1$s" class="widget %2$s">',
            'after_widget' => '</section>',
            'before_title' => '<h3 class="widget-title">',
            'after_title' => '</h3>',
        ));
        
        register_sidebar(array(
            'name' => esc_html__('Footer Widgets', '{{PROJECT_NAME}}'),
            'id' => 'sidebar-footer',
            'description' => esc_html__('Add widgets here to appear in your footer.', '{{PROJECT_NAME}}'),
            'before_widget' => '<div id="%1$s" class="footer-widget %2$s">',
            'after_widget' => '</div>',
            'before_title' => '<h4 class="footer-widget-title">',
            'after_title' => '</h4>',
        ));
    }
    
    /**
     * Customize register
     */
    public function customize_register($wp_customize) {
        // Add custom color scheme section
        $wp_customize->add_section('{{PROJECT_NAME}}_colors', array(
            'title' => esc_html__('Theme Colors', '{{PROJECT_NAME}}'),
            'priority' => 30,
        ));
        
        // Primary color setting
        $wp_customize->add_setting('primary_color', array(
            'default' => '#007cba',
            'sanitize_callback' => 'sanitize_hex_color',
        ));
        
        $wp_customize->add_control(
            new WP_Customize_Color_Control(
                $wp_customize,
                'primary_color',
                array(
                    'label' => esc_html__('Primary Color', '{{PROJECT_NAME}}'),
                    'section' => '{{PROJECT_NAME}}_colors',
                )
            )
        );
    }
    
    /**
     * Register custom post types
     */
    private function register_custom_post_types() {
        // Example: Portfolio post type
        register_post_type('portfolio', array(
            'labels' => array(
                'name' => esc_html__('Portfolio', '{{PROJECT_NAME}}'),
                'singular_name' => esc_html__('Portfolio Item', '{{PROJECT_NAME}}'),
                'add_new' => esc_html__('Add New', '{{PROJECT_NAME}}'),
                'add_new_item' => esc_html__('Add New Portfolio Item', '{{PROJECT_NAME}}'),
                'edit_item' => esc_html__('Edit Portfolio Item', '{{PROJECT_NAME}}'),
                'new_item' => esc_html__('New Portfolio Item', '{{PROJECT_NAME}}'),
                'view_item' => esc_html__('View Portfolio Item', '{{PROJECT_NAME}}'),
                'search_items' => esc_html__('Search Portfolio', '{{PROJECT_NAME}}'),
                'not_found' => esc_html__('No portfolio items found.', '{{PROJECT_NAME}}'),
                'not_found_in_trash' => esc_html__('No portfolio items found in Trash.', '{{PROJECT_NAME}}'),
            ),
            'public' => true,
            'publicly_queryable' => true,
            'show_ui' => true,
            'show_in_menu' => true,
            'query_var' => true,
            'rewrite' => array('slug' => 'portfolio'),
            'capability_type' => 'post',
            'has_archive' => true,
            'hierarchical' => false,
            'menu_position' => null,
            'menu_icon' => 'dashicons-portfolio',
            'supports' => array('title', 'editor', 'author', 'thumbnail', 'excerpt', 'comments'),
            'show_in_rest' => true, // Gutenberg support
        ));
    }
    
    /**
     * Register custom taxonomies
     */
    private function register_custom_taxonomies() {
        // Example: Portfolio categories
        register_taxonomy('portfolio_category', 'portfolio', array(
            'labels' => array(
                'name' => esc_html__('Portfolio Categories', '{{PROJECT_NAME}}'),
                'singular_name' => esc_html__('Portfolio Category', '{{PROJECT_NAME}}'),
                'search_items' => esc_html__('Search Categories', '{{PROJECT_NAME}}'),
                'all_items' => esc_html__('All Categories', '{{PROJECT_NAME}}'),
                'parent_item' => esc_html__('Parent Category', '{{PROJECT_NAME}}'),
                'parent_item_colon' => esc_html__('Parent Category:', '{{PROJECT_NAME}}'),
                'edit_item' => esc_html__('Edit Category', '{{PROJECT_NAME}}'),
                'update_item' => esc_html__('Update Category', '{{PROJECT_NAME}}'),
                'add_new_item' => esc_html__('Add New Category', '{{PROJECT_NAME}}'),
                'new_item_name' => esc_html__('New Category Name', '{{PROJECT_NAME}}'),
                'menu_name' => esc_html__('Categories', '{{PROJECT_NAME}}'),
            ),
            'hierarchical' => true,
            'public' => true,
            'publicly_queryable' => true,
            'show_ui' => true,
            'show_admin_column' => true,
            'query_var' => true,
            'rewrite' => array('slug' => 'portfolio-category'),
            'show_in_rest' => true,
        ));
    }
}

// Initialize theme
new {{PROJECT_NAME}}_Theme();

/**
 * Custom template tags for this theme
 */

/**
 * Display navigation to next/previous set of posts when applicable.
 */
function {{PROJECT_NAME}}_posts_navigation() {
    the_posts_navigation(array(
        'prev_text' => esc_html__('Older posts', '{{PROJECT_NAME}}'),
        'next_text' => esc_html__('Newer posts', '{{PROJECT_NAME}}'),
    ));
}

/**
 * Display navigation to next/previous post when applicable.
 */
function {{PROJECT_NAME}}_post_navigation() {
    the_post_navigation(array(
        'prev_text' => esc_html__('Previous: %title', '{{PROJECT_NAME}}'),
        'next_text' => esc_html__('Next: %title', '{{PROJECT_NAME}}'),
    ));
}

/**
 * Display posted on date.
 */
function {{PROJECT_NAME}}_posted_on() {
    $time_string = '<time class="entry-date published updated" datetime="%1$s">%2$s</time>';
    if (get_the_time('U') !== get_the_modified_time('U')) {
        $time_string = '<time class="entry-date published" datetime="%1$s">%2$s</time><time class="updated" datetime="%3$s">%4$s</time>';
    }

    $time_string = sprintf($time_string,
        esc_attr(get_the_date(DATE_W3C)),
        esc_html(get_the_date()),
        esc_attr(get_the_modified_date(DATE_W3C)),
        esc_html(get_the_modified_date())
    );

    printf('<span class="posted-on">%1$s <a href="%2$s" rel="bookmark">%3$s</a></span>',
        esc_html__('Posted on', '{{PROJECT_NAME}}'),
        esc_url(get_permalink()),
        $time_string
    );
}

/**
 * Display posted by author.
 */
function {{PROJECT_NAME}}_posted_by() {
    printf('<span class="byline">%1$s <span class="author vcard"><a class="url fn n" href="%2$s">%3$s</a></span></span>',
        esc_html__('by', '{{PROJECT_NAME}}'),
        esc_url(get_author_posts_url(get_the_author_meta('ID'))),
        esc_html(get_the_author())
    );
}

/**
 * Custom excerpt length
 */
function {{PROJECT_NAME}}_excerpt_length($length) {
    return 20;
}
add_filter('excerpt_length', '{{PROJECT_NAME}}_excerpt_length');

/**
 * Custom excerpt more string
 */
function {{PROJECT_NAME}}_excerpt_more($more) {
    return '&hellip; <a href="' . esc_url(get_permalink()) . '">' . esc_html__('Read more', '{{PROJECT_NAME}}') . '</a>';
}
add_filter('excerpt_more', '{{PROJECT_NAME}}_excerpt_more');