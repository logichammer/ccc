# /elementor-testimonial-slider

**Purpose**  
Create an HTML+CSS testimonial slider optimized for Elementor HTML widget with accessibility and responsiveness.

**Tags**: wordpress, elementor, testimonials, slider, html, css, accessible

**Arguments**
- `testimonials_data` (optional): JSON file with testimonial data or inline data
- `style_theme` (optional): Visual theme - modern, classic, minimal (default: modern)
- `autoplay` (optional): Enable auto-advance - true/false (default: true)
- `show_navigation` (optional): Show navigation arrows - true/false (default: true)

**Usage Example**
```
/elementor-testimonial-slider testimonials_data=testimonials.json style_theme=modern autoplay=true
```

**MCPs Used**
- File MCP: Load testimonial data
- Screenshot-website-fast: Visual verification

**Output**
Complete HTML/CSS/JS testimonial slider ready for Elementor HTML widget.

---

## Arguments

- Provide arguments inline as `key=value` pairs.
- Booleans: `true`/`false`. Lists: comma‑separated (no spaces) unless noted.

testimonials_data (optional): Path to JSON file or inline testimonial data
style_theme (optional): Visual theme - modern,classic,minimal (default: modern)
autoplay (boolean, default: true): Enable automatic slide advancement
autoplay_delay (number, default: 5000): Delay between slides in milliseconds
show_navigation (boolean, default: true): Display navigation arrows
show_indicators (boolean, default: true): Show slide indicator dots
animation_type (optional): Transition animation - slide,fade,zoom (default: slide)

---

## Runbook

### Phase 1: Data Processing
1. **Load Testimonial Data**:
   - Parse JSON file or process inline testimonial data
   - Validate required fields (name, testimonial, optional: title, company, image)
   - Handle missing or invalid data gracefully
   - Support multiple data formats

2. **Data Structure Validation**:
   ```json
   {
     "testimonials": [
       {
         "name": "John Doe",
         "title": "CEO",
         "company": "Tech Corp",
         "testimonial": "Amazing service and support!",
         "image": "path/to/image.jpg",
         "rating": 5
       }
     ]
   }
   ```

### Phase 2: HTML Structure Generation
1. **Semantic HTML Creation**:
   - Create accessible slider structure
   - Include proper ARIA labels and roles
   - Add skip links for keyboard navigation
   - Implement semantic markup for testimonials

2. **HTML Template**:
   ```html
   <div class="testimonial-slider" role="region" aria-label="Customer testimonials">
     <div class="slider-container">
       <div class="testimonial-slides" aria-live="polite">
         <!-- Dynamic testimonial slides -->
       </div>
       <button class="nav-btn prev" aria-label="Previous testimonial">‹</button>
       <button class="nav-btn next" aria-label="Next testimonial">›</button>
     </div>
     <div class="slider-indicators" role="tablist">
       <!-- Dynamic indicator dots -->
     </div>
   </div>
   ```

### Phase 3: CSS Styling
1. **Theme-Based Styling**:
   - Modern: Clean lines, subtle shadows, modern typography
   - Classic: Traditional borders, serif fonts, elegant spacing  
   - Minimal: Simple design, focus on content, minimal decorations

2. **Responsive Design**:
   - Mobile-first approach
   - Flexible image handling
   - Adaptive text sizing
   - Touch-friendly navigation

3. **CSS Structure**:
   ```css
   .testimonial-slider {
     max-width: 800px;
     margin: 0 auto;
     position: relative;
   }
   
   .testimonial-slide {
     display: none;
     text-align: center;
     padding: 2rem;
   }
   
   .testimonial-slide.active {
     display: block;
   }
   
   .testimonial-content {
     font-style: italic;
     font-size: 1.1rem;
     margin-bottom: 1.5rem;
   }
   
   .testimonial-author {
     font-weight: bold;
     color: #333;
   }
   ```

### Phase 4: JavaScript Functionality
1. **Core Slider Logic**:
   - Smooth transitions between slides
   - Keyboard navigation support (arrow keys)
   - Touch/swipe support for mobile
   - Auto-advance with pause on hover

2. **Accessibility Features**:
   - Screen reader announcements
   - Focus management
   - Reduced motion support
   - High contrast mode compatibility

3. **JavaScript Template**:
   ```javascript
   class TestimonialSlider {
     constructor(container, options = {}) {
       this.container = container;
       this.slides = container.querySelectorAll('.testimonial-slide');
       this.currentSlide = 0;
       this.autoplay = options.autoplay || true;
       this.delay = options.delay || 5000;
       
       this.init();
     }
     
     init() {
       this.createIndicators();
       this.bindEvents();
       if (this.autoplay) this.startAutoplay();
     }
     
     nextSlide() {
       this.goToSlide((this.currentSlide + 1) % this.slides.length);
     }
     
     prevSlide() {
       this.goToSlide((this.currentSlide - 1 + this.slides.length) % this.slides.length);
     }
   }
   ```

### Phase 5: Integration and Testing
1. **Elementor Integration**:
   - Package as single HTML widget code
   - Include all CSS and JS inline for portability
   - Test in Elementor editor preview
   - Verify responsive behavior

2. **Browser Testing**:
   - Cross-browser compatibility
   - Mobile device testing
   - Performance optimization
   - Loading state handling

### Phase 6: Customization Options
1. **Style Customization**:
   - Color scheme options
   - Font family selections
   - Spacing and sizing variables
   - Custom CSS hooks

2. **Functional Customization**:
   - Transition effects
   - Timing adjustments
   - Navigation styles
   - Content formatting

## Default Testimonial Data
If no data provided, include sample testimonials:
```json
{
  "testimonials": [
    {
      "name": "Sarah Johnson",
      "title": "Marketing Director",
      "company": "Digital Solutions Inc.",
      "testimonial": "Outstanding service and incredible attention to detail. The team exceeded our expectations in every way.",
      "rating": 5
    },
    {
      "name": "Michael Chen", 
      "title": "Founder",
      "company": "Tech Startup Co.",
      "testimonial": "Professional, reliable, and innovative. They transformed our vision into reality with remarkable skill.",
      "rating": 5
    },
    {
      "name": "Emily Rodriguez",
      "title": "Operations Manager", 
      "company": "Growth Agency",
      "testimonial": "The quality of work and level of communication was exceptional. Highly recommend their services.",
      "rating": 5
    }
  ]
}
```

## Error Handling

- Handle missing testimonial data with graceful fallback
- Validate JSON structure and provide clear error messages
- Include loading states for dynamic content
- Provide alternative text for images that fail to load

## Notes

- Code is copy-pastable directly into Elementor HTML widget
- All styles are scoped to prevent conflicts
- Includes prefers-reduced-motion support for accessibility
- Touch events optimized for mobile experience
- SEO-friendly with proper schema markup
- Performance optimized with lazy loading for images
- Includes comprehensive inline documentation